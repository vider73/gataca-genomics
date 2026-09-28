"""Genomics G1, step 1: a bacterial genome as a 2-bit stream with per-base gene-structure labels.

Downloads (and caches) the RefSeq genome FASTA + GFF annotation from NCBI, takes the main chromosome,
and writes, in data/genome_<name>/:
  symbols.npy   uint8 [L]  bases as symbols, project mapping G=0, A=1, T=2, C=3 (other letters -> 0, counted)
  labels.npy    uint8 [L]  0 = non-coding; 1..3 = forward-strand CDS, codon position 1..3;
                           4..6 = reverse-strand CDS, codon position 1..3 (counted on the reverse strand)
  split.npy     uint8 [L]  0 = train, 1 = validation, 2 = test (100 kb blocks, 8/1/1, fixed seed)
  genes.npy     int64 [G, 3]  CDS (start, end, strand) 0-based inclusive; strand +1 / -1
  meta.json
Where CDS overlap, the later one in the GFF wins (counted). Only single-segment CDS without a
partial flag and with a length divisible by 3 are used (the rest are counted and skipped).

--panel prepares the whole multi-species PANEL: each taxon is resolved to its RefSeq reference
assembly through the NCBI Datasets API, and data/panel.json records each genome's role (train = its
train blocks are used for training; test = held-out species, never trained on). A genome whose CDS
do not end in TAA/TAG/TGA >= 95% of the time (e.g. a different genetic code) is rejected.
"""

import argparse
import gzip
import json
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

from gataca import run_dir, update_metrics

GENOMES = {
    "ecoli": "GCF_000005845.2_ASM584v2",  # E. coli K-12 MG1655
    "bsubtilis": "GCF_000009045.1_ASM904v1",  # B. subtilis 168
}
# Diverse panel: GC from ~29% to ~72%, several phyla and two archaea. Species with genetic code 4
# (Mycoplasma & co.) are avoided. name: (NCBI taxon, role)
PANEL = {
    "ecoli": ("Escherichia coli str. K-12 substr. MG1655", "train"),
    "cjejuni": ("Campylobacter jejuni subsp. jejuni NCTC 11168 = ATCC 700819", "train"),
    "cdifficile": ("Clostridioides difficile 630", "train"),
    "saureus": ("Staphylococcus aureus subsp. aureus NCTC 8325", "train"),
    "hpylori": ("Helicobacter pylori 26695", "train"),
    "lmonocytogenes": ("Listeria monocytogenes EGD-e", "train"),
    "vcholerae": ("Vibrio cholerae O1 biovar El Tor str. N16961", "train"),
    "synechocystis": ("Synechocystis sp. PCC 6803", "train"),
    "styphimurium": ("Salmonella enterica subsp. enterica serovar Typhimurium str. LT2", "train"),
    "paeruginosa": ("Pseudomonas aeruginosa PAO1", "train"),
    "mtuberculosis": ("Mycobacterium tuberculosis H37Rv", "train"),
    "scoelicolor": ("Streptomyces coelicolor A3(2)", "train"),
    "mjannaschii": ("Methanocaldococcus jannaschii DSM 2661", "train"),
    # held-out species
    "bsubtilis": ("Bacillus subtilis subsp. subtilis str. 168", "test"),
    "spneumoniae": ("Streptococcus pneumoniae TIGR4", "test"),
    "dradiodurans": ("Deinococcus radiodurans R1 = ATCC 13939 = DSM 20539", "test"),
    "tthermophilus": ("Thermus thermophilus HB8", "test"),
    "hvolcanii": ("Haloferax volcanii DS2", "test"),
}
BASE_TO_SYMBOL = {"G": 0, "A": 1, "T": 2, "C": 3}
BLOCK = 100_000


def ncbi_url(assembly: str, suffix: str) -> str:
    acc = assembly.split("_")[0] + "_" + assembly.split("_")[1]  # GCF_000005845.2
    digits = acc.split("_")[1].split(".")[0]
    path = "/".join([digits[i : i + 3] for i in range(0, 9, 3)])
    return f"https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/{path}/{assembly}/{assembly}_{suffix}"


def resolve_taxon(taxon: str) -> str:
    """RefSeq reference assembly '<accession>_<assembly name>' for a taxon, via the NCBI Datasets API."""
    for extra in ("&filters.reference_only=true", ""):
        url = ("https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/" + urllib.parse.quote(taxon)
               + "/dataset_report?filters.assembly_source=refseq&filters.assembly_level=complete_genome" + extra)
        reports = json.loads(urllib.request.urlopen(url, timeout=60).read()).get("reports", [])
        if reports:
            r = reports[0]
            return f"{r['accession']}_{r['assembly_info']['assembly_name']}".replace(" ", "_")
    raise LookupError(f"no RefSeq complete genome for {taxon!r}")


def fetch(url: str, cache: Path) -> bytes:
    if not cache.exists():
        print(f"downloading {url}")
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    return gzip.decompress(cache.read_bytes())


def read_main_chromosome(fasta: str):
    records, name, seq = {}, None, []
    for line in fasta.splitlines():
        if line.startswith(">"):
            if name:
                records[name] = "".join(seq)
            name, seq = line[1:].split()[0], []
        else:
            seq.append(line.strip().upper())
    records[name] = "".join(seq)
    main = max(records, key=lambda k: len(records[k]))
    return main, records[main]


def read_cds(gff: str, seqid: str):
    """CDS rows of seqid, grouped by ID so multi-segment CDS (e.g. ribosomal frameshifts) can be skipped."""
    by_id = {}
    for line in gff.splitlines():
        if line.startswith("#"):
            continue
        f = line.split("\t")
        if len(f) < 9 or f[0] != seqid or f[2] != "CDS":
            continue
        attrs = dict(kv.split("=", 1) for kv in f[8].split(";") if "=" in kv)
        by_id.setdefault(attrs.get("ID", line), []).append(
            (int(f[3]) - 1, int(f[4]) - 1, 1 if f[6] == "+" else -1, attrs))
    return by_id


def prepare(name: str, assembly: str, seed: int, runs_dir: Path, force: bool = False) -> dict:
    out = Path("data") / f"genome_{name}"
    if (out / "meta.json").exists() and not force:
        stats = json.loads((out / "meta.json").read_text())
        if "stop_codon_ok" in stats:
            return stats
    out.mkdir(parents=True, exist_ok=True)
    fasta = fetch(ncbi_url(assembly, "genomic.fna.gz"), out / "raw" / f"{assembly}_genomic.fna.gz").decode()
    gff = fetch(ncbi_url(assembly, "genomic.gff.gz"), out / "raw" / f"{assembly}_genomic.gff.gz").decode()
    seqid, seq = read_main_chromosome(fasta)
    L = len(seq)

    symbols = np.array([BASE_TO_SYMBOL.get(c, 0) for c in seq], dtype=np.uint8)
    non_acgt = sum(c not in BASE_TO_SYMBOL for c in seq)

    labels = np.zeros(L, dtype=np.uint8)
    genes, skipped = [], {"multi_segment": 0, "partial": 0, "not_multiple_of_3": 0, "pseudo": 0}
    written = np.zeros(L, dtype=bool)
    overlap_bases = 0
    for rows in read_cds(gff, seqid).values():
        if len(rows) > 1:
            skipped["multi_segment"] += 1
            continue
        start, end, strand, attrs = rows[0]
        if end >= L or start < 0:  # a gene wrapping the origin of a circular chromosome
            skipped["wraps_origin"] = skipped.get("wraps_origin", 0) + 1
            continue
        if attrs.get("partial") == "true" or "start_range" in attrs or "end_range" in attrs:
            skipped["partial"] += 1
            continue
        if attrs.get("pseudo") == "true":
            skipped["pseudo"] += 1
            continue
        if (end - start + 1) % 3:
            skipped["not_multiple_of_3"] += 1
            continue
        idx = np.arange(start, end + 1)
        codon_pos = (idx - start) % 3 if strand == 1 else (end - idx) % 3
        overlap_bases += int(written[idx].sum())
        labels[idx] = codon_pos + (1 if strand == 1 else 4)
        written[idx] = True
        genes.append((start, end, strand))
    genes = np.array(sorted(genes), dtype=np.int64)

    rng = np.random.default_rng(seed)
    n_blocks = -(-L // BLOCK)
    block_split = rng.permutation(np.array(([0] * 8 + [1] + [2]) * (n_blocks // 10 + 1))[:n_blocks])
    split = np.repeat(block_split, BLOCK)[:L].astype(np.uint8)

    np.save(out / "symbols.npy", symbols)
    np.save(out / "labels.npy", labels)
    np.save(out / "split.npy", split)
    np.save(out / "genes.npy", genes)
    seq_str = seq
    comp = str.maketrans("ACGT", "TGCA")
    stop_ok = np.mean([(seq_str[a : b + 1] if st == 1 else seq_str[a : b + 1].translate(comp)[::-1])[-3:]
                       in ("TAA", "TAG", "TGA") for a, b, st in genes]) if len(genes) else 0.0
    stats = {
        "genome": name, "assembly": assembly, "stop_codon_ok": float(stop_ok), "seqid": seqid, "length": L, "non_acgt": non_acgt,
        "gc": float(np.isin(symbols, [0, 3]).mean()),
        "cds_used": len(genes), "cds_skipped": skipped, "coding_frac": float((labels > 0).mean()),
        "forward_frac": float(((labels >= 1) & (labels <= 3)).mean()), "overlap_bases": overlap_bases,
        "split_bases": {s: int((split == i).sum()) for i, s in enumerate(["train", "validation", "test"])},
    }
    (out / "meta.json").write_text(json.dumps(stats, indent=2))
    update_metrics(run_dir(runs_dir), f"prepare_genome/{name}", stats)
    return stats


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--genome", choices=[*GENOMES, *PANEL], default="ecoli")
    p.add_argument("--panel", action="store_true", help="prepare every genome in PANEL and write data/panel.json")
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    if not args.panel:
        assembly = GENOMES.get(args.genome) or resolve_taxon(PANEL[args.genome][0])
        print(json.dumps(prepare(args.genome, assembly, args.seed, args.runs_dir), indent=2))
        return

    panel = {}
    for name, (taxon, role) in PANEL.items():
        try:
            assembly = GENOMES.get(name) or resolve_taxon(taxon)
            st = prepare(name, assembly, args.seed, args.runs_dir)
        except Exception as e:  # network, missing assembly, parsing: report and go on
            print(f"{name:>16}: FAILED {e.__class__.__name__}: {e}")
            continue
        ok = st["stop_codon_ok"] >= 0.95 and st["cds_used"] > 500
        print(f"{name:>16}: {st['assembly']:<32} {st['length']:>9,} bp  GC {st['gc']:.1%}  CDS {st['cds_used']:>5}  "
              f"stop ok {st['stop_codon_ok']:.3f}  {role}{'' if ok else '  REJECTED'}")
        if ok:
            panel[name] = {"role": role, "assembly": st["assembly"], "gc": st["gc"], "length": st["length"],
                           "cds": st["cds_used"]}
    Path("data/panel.json").write_text(json.dumps(panel, indent=2))
    print(f"wrote data/panel.json: {sum(v['role'] == 'train' for v in panel.values())} train, "
          f"{sum(v['role'] == 'test' for v in panel.values())} test genomes")


if __name__ == "__main__":
    main()
