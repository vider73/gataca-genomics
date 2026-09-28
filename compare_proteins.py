"""Genomics G1, practical test: which method recovers the real proteins from raw nanopore reads?

Every method gets the reads one by one, before assembly, and outputs proteins:
  organ checkpoints   per-base labels (argmax, and the grammar decoder); each same-strand run of coding
                      labels is translated with the organ's own codon positions, so frameshifts are
                      corrected: a base that repeats a codon position is dropped (insertion), a codon
                      with a missing position becomes X (deletion). Runs are not split at frame breaks.
  prodigal            Prodigal in metagenomic mode, genes translated as called (no frame correction)
  fgs_<model>         FragGeneScanRs (WSL) with a sequencing-error model (454_10, 454_30, sanger_10, ...)
  diamond_<db>        DIAMOND blastx --long-reads (frameshift-aware, -F 15) against a protein database;
                      each kept hit's translated read segment is a predicted protein. Databases:
                        panel  proteins of the 13 training species (what the organ saw: no close reference)
                        self   the held-out genome's own proteome (an oracle upper bound, not a fair method)

Scoring (DIAMOND blastp of predicted proteins >= 30 aa against the true proteins of genes touching the
read; a hit only counts if the predicted protein lies on that gene's reference span and strand):
  recovered     reference genes lying fully inside a read whose protein is matched with >= 80% coverage
                and >= 80% identity by a single predicted protein
  score         mean over those genes of the best identity x coverage (0 if not found)
  precision     predicted proteins that match any gene touching the read (partial genes included, so
                genes cut by read ends are not counted as false) with >= 80% identity over >= 50% of
                the predicted protein

Predicted proteins are cached in runs/<date>/proteins/<run>/<target>.faa (--recompute to redo), so CPU
methods and organs (GPU; launch those through I:/LLMLab/GPUControl/gpu.py) can run separately.
Writes runs/<date>/proteins_<genome>.md and metrics.json under "compare_proteins/<run>/<target>".
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

import numpy as np

from eval_genome import grammar_decode, prodigal_genes, revcomp, to_seq
from gataca import Progress, genes_to_labels, run_dir, update_metrics

DIAMOND = Path("tools/diamond/diamond.exe")
FGS = "tools/fgsrs/FragGeneScanRs"
BASES = "TCAG"
AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"  # standard / bacterial code 11
CODE = {a + b + c: AA[16 * i + 4 * j + k] for i, a in enumerate(BASES) for j, b in enumerate(BASES)
        for k, c in enumerate(BASES)}


def translate(dna: str) -> str:
    return "".join(CODE.get(dna[i : i + 3], "X") for i in range(0, len(dna) - 2, 3))


def wsl_path(p: Path) -> str:
    p = p.resolve()
    return f"/mnt/{p.drive[0].lower()}{p.as_posix()[2:]}"


def labelled_protein(seq: str, pos: np.ndarray) -> str:
    """Translate bases carrying codon positions 1..3 (in reading order), correcting frameshifts."""
    out, codon = [], {}
    last = 0
    for base, p in zip(seq, pos):
        if p == last:  # the same position again: an extra (inserted) base
            continue
        if p < last:  # the cycle restarted: close the codon (a missing position makes it X)
            out.append(CODE.get("".join(codon.get(k, "N") for k in (1, 2, 3)), "X"))
            codon = {}
        codon[p] = base
        last = p
    if len(codon) == 3:
        out.append(CODE.get(codon[1] + codon[2] + codon[3], "X"))
    return "".join(out)


def organ_proteins(seq: str, labels: np.ndarray, min_len=90):
    """Same-strand runs of coding labels -> (start, end, strand, protein), frame-corrected by the labels."""
    out, i, L = [], 0, len(labels)
    while i < L:
        if labels[i] == 0:
            i += 1
            continue
        fwd = labels[i] <= 3
        j = i
        while j < L and labels[j] > 0 and (labels[j] <= 3) == fwd:
            j += 1
        if j - i >= min_len:
            if fwd:
                prot = labelled_protein(seq[i:j], labels[i:j])
            else:
                prot = labelled_protein(revcomp(seq[i:j]), labels[i:j][::-1] - 3)
            out.append((i, j - 1, 1 if fwd else -1, prot.strip("*")))
        i = j
    return out


def cds_protein(seq: str, a: int, b: int, strand: int) -> str:
    dna = seq[a : b + 1] if strand == 1 else revcomp(seq[a : b + 1])
    return translate(dna[: len(dna) // 3 * 3]).rstrip("*")


def ref_span(a, b, refpos):
    """Read coordinates -> reference span of the kept (non-inserted) bases inside."""
    rp = refpos[a : b + 1]
    rp = rp[rp >= 0]
    return (int(rp.min()), int(rp.max())) if len(rp) else None


def write_faa(path: Path, records):
    with path.open("w") as f:
        for name, prot in records:
            f.write(f">{name}\n{prot}\n")


def read_faa(path: Path):
    name, seqs = None, {}
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            name = line[1:].split()[0]
            seqs[name] = []
        elif name:
            seqs[name].append(line.strip())
    return {k: "".join(v) for k, v in seqs.items()}


def run_diamond(args):
    # stdin=DEVNULL: detached jobs (scheduled tasks) have no console handle to inherit
    return subprocess.run([str(DIAMOND), *args], capture_output=True, text=True, check=True,
                          stdin=subprocess.DEVNULL).stdout


def build_db(fasta: Path, db: Path):
    if not db.with_suffix(".dmnd").exists():
        run_diamond(["makedb", "--in", str(fasta), "-d", str(db), "--quiet"])


def genome_proteome(name: str, prefix: str):
    d = Path("data") / f"genome_{name}"
    seq = to_seq(np.load(d / "symbols.npy"))
    return [(f"{prefix}{k}", cds_protein(seq, int(a), int(b), int(s))) for k, (a, b, s) in enumerate(np.load(d / "genes.npy"))]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("targets", nargs="+", help="organ checkpoints, prodigal, fgs_<model>, diamond_panel, diamond_self")
    p.add_argument("--runs", nargs="+", required=True)
    p.add_argument("--genome", default="hvolcanii")
    p.add_argument("--max-bases", type=float, default=4e6)
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--recompute", action="store_true")
    p.add_argument("--score-only", action="store_true", help="only score the cached proteins of every target")
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    p.add_argument("--proteins-dir", type=Path, default=None,
                   help="protein cache to reuse (default runs/<date>/proteins), e.g. to add organs on a later day")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    out_dir = run_dir(args.runs_dir)
    work = args.proteins_dir or out_dir / "proteins"
    work.mkdir(exist_ok=True)
    gdir = Path("data") / f"genome_{args.genome}"
    ref_seq = to_seq(np.load(gdir / "symbols.npy"))
    ref_genes = [tuple(int(x) for x in g) for g in np.load(gdir / "genes.npy")]
    starts = np.array([g[0] for g in ref_genes])
    panel = json.loads(Path("data/panel.json").read_text())

    # Reference protein databases for DIAMOND blastx.
    dbs = {}
    for t in args.targets:
        if t.startswith("diamond_"):
            which = t.removeprefix("diamond_")
            fa = work / f"db_{which}.faa"
            if not fa.exists():
                names = [n for n, v in panel.items() if v["role"] == "train"] if which == "panel" else [args.genome]
                write_faa(fa, [r for n in names for r in genome_proteome(n, f"{n}_") if len(r[1]) >= 30])
            build_db(fa, work / f"db_{which}")
            dbs[t] = work / f"db_{which}"
    models = {}
    for t in args.targets:
        if t.endswith(".pt"):
            import torch
            from gataca import load_segmenter
            models[t] = load_segmenter(Path(t), "cuda" if torch.cuda.is_available() else "cpu")[0]

    rows = []
    for run in args.runs:
        d = Path("data/nanopore") / run
        sym, refpos, offsets = np.load(d / "symbols.npy"), np.load(d / "refpos.npy"), np.load(d / "offsets.npy")
        meta = json.loads((d / "meta.json").read_text())
        order = np.random.default_rng(args.seed).permutation(len(offsets) - 1)  # same reads as eval_nanopore
        picked, total = [], 0
        for i in order:
            picked.append(int(i))
            total += offsets[i + 1] - offsets[i]
            if total >= args.max_bases:
                break
        rdir = work / run
        rdir.mkdir(exist_ok=True)
        reads = {f"r{i}": (to_seq(sym[offsets[i] : offsets[i + 1]]), refpos[offsets[i] : offsets[i + 1]]) for i in picked}
        reads_fa = rdir / "reads.fna"
        if not reads_fa.exists():
            write_faa(reads_fa, [(k, s) for k, (s, _) in reads.items()])

        # Truth: complete genes inside each read (recall) and every gene touching it (precision, scoring DB).
        complete, touching = {}, {}
        for k, (_, rp) in reads.items():
            lo, hi = int(rp[rp >= 0].min()), int(rp[rp >= 0].max())
            idx = [j for j in np.flatnonzero(starts <= hi) if ref_genes[j][1] >= lo]
            touching[k] = idx
            complete[k] = [j for j in idx if ref_genes[j][0] >= lo and ref_genes[j][1] <= hi]
        truth_fa = rdir / "truth.faa"
        all_touch = sorted({j for v in touching.values() for j in v})
        if not truth_fa.exists():
            write_faa(truth_fa, [(f"g{j}", cds_protein(ref_seq, *ref_genes[j])) for j in all_touch])
        build_db(truth_fa, rdir / "truth")

        # Predictions per target: name -> (read, ref span, strand, protein).
        targets = [t for t in args.targets] if not args.score_only else \
            sorted(f.stem for f in rdir.glob("*.faa") if f.stem != "truth" and not f.stem.startswith("raw_"))
        for t in args.targets if not args.score_only else []:
            names = [Path(t).stem, f"{Path(t).stem}+decoder"] if t.endswith(".pt") else [t]
            if all((rdir / f"{n}.faa").exists() for n in names) and not args.recompute:
                continue
            recs = {n: [] for n in names}
            if t.endswith(".pt"):
                import torch
                from gataca import tag_stream
                progress = Progress(args.runs_dir, f"proteins_{run}_{Path(t).stem}", len(reads), "compare_proteins")
                for n_read, (k, (s, rp)) in enumerate(reads.items()):
                    device = next(models[t].parameters()).device
                    x = torch.from_numpy(np.array(["GATC".index(c) for c in s], dtype=np.int64)).to(device)
                    logits = tag_stream(models[t], x)
                    for n, lab in zip(names, (logits.argmax(-1).cpu().numpy(), grammar_decode(logits, s))):
                        for a, b, st, prot in organ_proteins(s, lab):
                            span = ref_span(a, b, rp)
                            if span and len(prot) >= 30:
                                recs[n].append((f"{k}|{span[0]}|{span[1]}|{st}|{len(recs[n])}", prot))
                    progress.update(n_read + 1)
                progress.done()
            elif t == "prodigal":
                progress = Progress(args.runs_dir, f"proteins_{run}_prodigal", len(reads), "compare_proteins")
                for n_read, (k, (s, rp)) in enumerate(reads.items()):
                    for a, b, st in prodigal_genes(s, meta=True):
                        span, prot = ref_span(a, b, rp), cds_protein(s, a, b, st)
                        if span and len(prot) >= 30:
                            recs[t].append((f"{k}|{span[0]}|{span[1]}|{st}|{len(recs[t])}", prot))
                    progress.update(n_read + 1)
                progress.done()
            elif t.startswith("fgs_"):
                faa = rdir / f"raw_{t}.faa"
                subprocess.run(["wsl", "-e", "bash", "-c",
                                f"{wsl_path(Path(FGS))} -s {wsl_path(reads_fa)} -a {wsl_path(faa)} -w 0 "
                                f"-t {t.removeprefix('fgs_')} -p {args.threads}"], check=True, stdin=subprocess.DEVNULL)
                for name, prot in read_faa(faa).items():
                    k, a, b, st = name.rsplit("_", 3)  # FragGeneScan: <read>_<start>_<end>_<strand>, 1-based
                    span = ref_span(int(a) - 1, int(b) - 1, reads[k][1])
                    prot = prot.strip("*")
                    if span and len(prot) >= 30:
                        recs[t].append((f"{k}|{span[0]}|{span[1]}|{1 if st == '+' else -1}|{len(recs[t])}", prot))
            elif t.startswith("diamond_"):
                tsv = rdir / f"raw_{t}.tsv"
                run_diamond(["blastx", "-q", str(reads_fa), "-d", str(dbs[t]), "-o", str(tsv), "--long-reads",
                             "--threads", str(args.threads), "--quiet", "--outfmt", "6", "qseqid", "qstart", "qend",
                             "bitscore", "qseq_translated"])
                hits = []
                for line in tsv.read_text().splitlines():
                    k, qs, qe, bits, prot = line.split("\t")
                    qs, qe = int(qs) - 1, int(qe) - 1
                    hits.append((float(bits), k, min(qs, qe), max(qs, qe), 1 if qe >= qs else -1, re.sub("[^A-Z*]", "", prot)))  # drop gaps and frameshift marks
                kept = {}
                for bits, k, a, b, st, prot in sorted(hits, reverse=True):  # one protein per read region
                    if any(st == s2 and min(b, b2) - max(a, a2) > 0.5 * (b - a) for a2, b2, s2 in kept.get(k, [])):
                        continue
                    kept.setdefault(k, []).append((a, b, st))
                    span = ref_span(a, b, reads[k][1])
                    if span and len(prot) >= 30:
                        recs[t].append((f"{k}|{span[0]}|{span[1]}|{st}|{len(recs[t])}", prot))
            else:
                raise SystemExit(f"unknown target {t}")
            for n in names:
                write_faa(rdir / f"{n}.faa", recs[n])
            print(f"{run} {t}: proteins written", flush=True)

        # Score every cached prediction set.
        stems = sorted({Path(t).stem for t in args.targets if t.endswith(".pt")} |
                       {f"{Path(t).stem}+decoder" for t in args.targets if t.endswith(".pt")} |
                       {t for t in args.targets if not t.endswith(".pt")}) if not args.score_only else targets
        n_complete = sum(len(v) for v in complete.values())
        for name in stems:
            faa = rdir / f"{name}.faa"
            preds = read_faa(faa)
            tsv = rdir / f"score_{name}.tsv"
            if preds:
                run_diamond(["blastp", "-q", str(faa), "-d", str(rdir / "truth"), "-o", str(tsv), "--sensitive",
                             "--max-target-seqs", "10", "--evalue", "1e-5", "--threads", str(args.threads), "--quiet",
                             "--outfmt", "6", "qseqid", "sseqid", "pident", "length", "sstart", "send", "slen", "qlen"])
            best, good_pred = {}, set()
            for line in (tsv.read_text().splitlines() if preds and tsv.exists() else []):
                q, s, pid, length, ss, se, slen, qlen = line.split("\t")
                k, lo, hi, st, _ = q.split("|")
                j = int(s[1:])
                g = ref_genes[j]
                if g[2] != int(st) or min(int(hi), g[1]) < max(int(lo), g[0]) or j not in touching[k]:
                    continue  # not this gene's location: a paralog or a chance hit
                pid, cov = float(pid) / 100, (int(se) - int(ss) + 1) / int(slen)
                if j in complete[k]:
                    best[(k, j)] = max(best.get((k, j), (0, 0, 0)), (pid * cov, pid, cov))
                if pid >= 0.8 and int(length) >= 0.5 * int(qlen):
                    good_pred.add(q)
            rec = sum(1 for v in best.values() if v[1] >= 0.8 and v[2] >= 0.8)
            res = {"genes": n_complete, "recovered": rec / max(1, n_complete),
                   "score": sum(v[0] for v in best.values()) / max(1, n_complete),
                   "proteins": len(preds), "precision": len(good_pred) / max(1, len(preds)),
                   "aa_predicted": int(sum(len(v) for v in preds.values()))}
            update_metrics(out_dir, f"compare_proteins/{run}/{name}", res)
            rows.append([run, f"{meta['identity']:.1%}", name, f"{res['recovered']:.3f}", f"{res['score']:.3f}",
                         f"{res['precision']:.3f}", str(res["proteins"]), str(n_complete)])
            print(run, name, json.dumps(res), flush=True)

    cols = ["run", "read identity", "method", "genes recovered (>=80% cov & id)", "mean id x cov",
            "precision", "proteins predicted", "genes in reads"]
    lines = [f"# Proteins recovered from raw nanopore reads — {args.genome}", "",
             "Each read on its own. diamond_self uses the held-out genome's own proteome: an oracle, not a fair method.",
             "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(r) + " |" for r in sorted(rows)]
    path = out_dir / f"proteins_{args.genome}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
