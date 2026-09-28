"""Genomics G1, real errors, step 1: align real nanopore reads to their reference chromosome.

For each run: minimap2 (map-ont, run inside WSL) aligns the reads to the main chromosome of the
genome. Primary alignments with MAPQ >= 20 covering >= 80% of the read are kept. Each kept read is
oriented to the reference's forward strand and trimmed to its aligned part. Every read base then
gets the reference position it came from, or -1 if the sequencer inserted it. Deleted reference
bases simply have no read base. That is the ground truth for scoring organs on real error-laden
reads.

Writes data/nanopore/<run>/:
  symbols.npy   uint8 [N]  all kept reads concatenated (G=0 A=1 T=2 C=3), reference-oriented
  refpos.npy    int64 [N]  reference position of each read base, -1 for inserted bases
  offsets.npy   int64 [R+1] read boundaries in the arrays above
  meta.json     read count, bases, identity (matches / alignment columns), error mix
"""

import argparse
import gzip
import json
import re
import subprocess
from pathlib import Path

import numpy as np

from gataca import DNA, dna_to_symbols, run_dir, update_metrics

MINIMAP2 = "tools/minimap2-2.31_x64-linux/minimap2"
COMP = str.maketrans("ACGT", "TGCA")


def wsl_path(p: Path) -> str:
    p = p.resolve()
    return f"/mnt/{p.drive[0].lower()}{p.as_posix()[2:]}"


def read_fastq(path: Path):
    with gzip.open(path, "rt") as f:
        while True:
            head = f.readline()
            if not head:
                return
            seq = f.readline().strip().upper()
            f.readline()
            f.readline()
            yield head[1:].split()[0], seq


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--run", required=True, help="run accession; reads in data/nanopore/raw/<run>.fastq.gz")
    p.add_argument("--genome", default="hvolcanii")
    p.add_argument("--min-mapq", type=int, default=20)
    p.add_argument("--min-cover", type=float, default=0.8)
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    args = p.parse_args()

    out = Path("data/nanopore") / args.run
    out.mkdir(parents=True, exist_ok=True)
    ref_sym = np.load(Path("data") / f"genome_{args.genome}" / "symbols.npy")
    ref = "".join(np.array(list(DNA))[ref_sym])
    ref_fa = Path("data/nanopore") / f"{args.genome}_ref.fa"
    if not ref_fa.exists():
        ref_fa.write_text(">ref\n" + "\n".join(ref[i : i + 80] for i in range(0, len(ref), 80)) + "\n")

    reads_gz = Path("data/nanopore/raw") / f"{args.run}.fastq.gz"
    paf = out / "aln.paf"
    if not paf.exists():
        cmd = f"{MINIMAP2} -x map-ont -c --cs -t {args.threads} --secondary=no {wsl_path(ref_fa)} {wsl_path(reads_gz)}"
        print("running minimap2 in WSL ...", flush=True)
        paf.write_bytes(subprocess.run(["wsl", "-e", "bash", "-c", f"cd {wsl_path(Path('.'))} && {cmd}"],
                                       capture_output=True, check=True).stdout)

    best = {}
    for line in paf.read_text().splitlines():
        f = line.split("\t")
        qname, qlen, qs, qe, strand, _, _, ts, te = f[0], int(f[1]), int(f[2]), int(f[3]), f[4], f[5], f[6], int(f[7]), int(f[8])
        mapq = int(f[11])
        tags = dict(t.split(":", 2)[::2] for t in f[12:])
        if tags.get("tp") != "P" or mapq < args.min_mapq or (qe - qs) < args.min_cover * qlen:
            continue
        best[qname] = (qs, qe, strand, ts, tags["cs"])

    syms, refpos, offsets = [], [], [0]
    n_match = n_sub = n_ins = n_del = 0
    n_reads_total = 0
    for name, seq in read_fastq(reads_gz):
        n_reads_total += 1
        if name not in best or set(seq) - set("ACGT"):
            continue
        qs, qe, strand, ts, cs = best[name]
        q = seq[qs:qe]
        if strand == "-":
            q = q.translate(COMP)[::-1]
        pos, qi, rp = ts, 0, []
        for op, val in re.findall(r"([:*+\-])([0-9]+|[a-z]+)", cs):
            if op == ":":
                n = int(val)
                rp.extend(range(pos, pos + n))
                pos += n
                qi += n
                n_match += n
            elif op == "*":  # substitution: ref base, read base
                rp.append(pos)
                pos += 1
                qi += 1
                n_sub += 1
            elif op == "+":  # bases only in the read
                rp.extend([-1] * len(val))
                qi += len(val)
                n_ins += len(val)
            else:  # "-": bases only in the reference
                pos += len(val)
                n_del += len(val)
        assert qi == len(q), (name, qi, len(q))
        syms.append(dna_to_symbols(q))
        refpos.append(np.array(rp, dtype=np.int64))
        offsets.append(offsets[-1] + len(q))

    np.save(out / "symbols.npy", np.concatenate(syms))
    np.save(out / "refpos.npy", np.concatenate(refpos))
    np.save(out / "offsets.npy", np.array(offsets, dtype=np.int64))
    cols = n_match + n_sub + n_ins + n_del
    stats = {"run": args.run, "genome": args.genome, "reads_total": n_reads_total, "reads_kept": len(syms),
             "bases_kept": int(offsets[-1]), "mean_read_len": float(offsets[-1] / max(1, len(syms))),
             "identity": n_match / max(1, cols), "sub_rate": n_sub / max(1, cols),
             "ins_rate": n_ins / max(1, cols), "del_rate": n_del / max(1, cols)}
    (out / "meta.json").write_text(json.dumps(stats, indent=2))
    update_metrics(run_dir(args.runs_dir), f"prepare_nanopore/{args.run}", stats)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
