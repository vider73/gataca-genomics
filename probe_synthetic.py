"""Genomics G1, probe: did the organ learn gene MECHANICS or E. coli's ACCENT?

Builds synthetic genomes out of three kinds of segment and scores organs and baselines on them:
  mechanics  real gene mechanics, no E. coli accent: ATG + random sense codons (no internal stop) + stop.
             Codons are drawn with a target GC (35/50/65%), not with E. coli's codon preferences.
  accent     E. coli's accent, no gene mechanics: codons drawn from E. coli's own codon usage
             (measured on its train-block genes), but with an in-frame stop every ~18 codons.
  filler     random DNA with the same GC.
Half of the mechanics and accent segments sit on the reverse strand.

An organ that learned the mechanics calls `mechanics` coding (in the right frame) and `accent` non-coding.
One that learned the accent does the opposite. The ORF rule is pure mechanics by construction.

Writes runs/<date>/synthetic_probe.md and metrics.json under "probe_synthetic/<target>/gc<GC>".
"""

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
import torch

from eval_genome import (base_scores, gene_scores, genes_from_labels, orf_genes, prodigal_genes,
                         stop_anchored_labels, to_seq)
from gataca import codon_usage, genes_to_labels, load_segmenter, run_dir, synthetic_dna, tag_stream, update_metrics

BASES = "GATC"
STOPS = ["TAA", "TAG", "TGA"]
CODONS = ["".join(c) for c in itertools.product("ACGT", repeat=3)]
SENSE = [c for c in CODONS if c not in STOPS]
COMP = str.maketrans("ACGT", "TGCA")


def gc_weights(codons, gc):
    w = np.array([np.prod([gc / 2 if b in "GC" else (1 - gc) / 2 for b in c]) for c in codons])
    return w / w.sum()


def ecoli_codon_usage():
    d = Path("data/genome_ecoli")
    return codon_usage(np.load(d / "symbols.npy"), [tuple(g) for g in np.load(d / "genes.npy")],
                       np.load(d / "split.npy") == 0)


def build(gc, n_segments, rng, ecoli_usage):
    parts, genes, kinds, pos = [], [], [], 0
    sense_w = gc_weights(SENSE, gc)
    base_p = np.array([gc / 2, (1 - gc) / 2, (1 - gc) / 2, gc / 2])  # G A T C

    def add(s, kind):
        nonlocal pos
        parts.append(s)
        kinds.append((pos, pos + len(s), kind))
        pos += len(s)

    for i in range(n_segments):
        add("".join(rng.choice(list(BASES), rng.integers(100, 400), p=base_p)), "filler")
        n_codons = int(rng.integers(100, 500))
        if i % 2 == 0:
            body = "".join(rng.choice(SENSE, n_codons, p=sense_w))
            s = "ATG" + body + rng.choice(STOPS)
            kind = "mechanics"
        else:
            codons = list(rng.choice(SENSE, n_codons, p=ecoli_usage))
            for k in np.cumsum(rng.geometric(1 / 18, n_codons)):
                if k < n_codons:
                    codons[k] = rng.choice(STOPS)
            s = "".join(codons)
            kind = "accent"
        strand = 1 if rng.random() < 0.5 else -1
        if strand == -1:
            s = s.translate(COMP)[::-1]
        if kind == "mechanics":
            genes.append((pos, pos + len(s) - 1, strand))
        add(s, kind)
    seq = "".join(parts)
    sym = np.array([BASES.index(c) for c in seq], dtype=np.uint8)
    return seq, sym, genes, kinds


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("targets", nargs="+", help="organ checkpoints and/or orf, prodigal")
    p.add_argument("--gc", nargs="+", type=float, default=[0.35, 0.50, 0.65])
    p.add_argument("--segments", type=int, default=600)
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    usage = ecoli_codon_usage()
    out_dir = run_dir(args.runs_dir)
    rows = []
    for gc in args.gc:
        sym, _, genes, kinds = synthetic_dna(gc, args.segments, np.random.default_rng(args.seed), usage)
        seq = to_seq(sym)
        L = len(sym)
        gold = genes_to_labels(L, genes)
        masks = {k: np.zeros(L, dtype=bool) for k in ("mechanics", "accent", "filler")}
        for a, b, k in kinds:
            masks[k][a:b] = True
        everywhere = np.ones(L, dtype=bool)
        for target in args.targets:
            name = target if target in ("orf", "prodigal") else Path(target).stem
            if target in ("orf", "prodigal"):
                pred_genes = orf_genes(seq) if target == "orf" else prodigal_genes(seq)
                pred = stop_anchored_labels(L, pred_genes)
            else:
                model = load_segmenter(Path(target), device)[0]
                pred = tag_stream(model, torch.from_numpy(sym.astype(np.int64)).to(device)).argmax(-1).cpu().numpy()
                pred_genes = genes_from_labels(pred)
            mech = base_scores(pred, gold, masks["mechanics"])
            res = {
                "mechanics_called_coding": float((pred[masks["mechanics"]] > 0).mean()),
                "mechanics_frame_acc": mech["frame_acc"],
                "accent_called_coding": float((pred[masks["accent"]] > 0).mean()),
                "filler_called_coding": float((pred[masks["filler"]] > 0).mean()),
                **{f"genes_{k}": v for k, v in gene_scores(pred_genes, genes, everywhere).items()},
            }
            update_metrics(out_dir, f"probe_synthetic/{name}/gc{int(gc * 100)}", res)
            print(f"gc {gc:.2f} {name}: {json.dumps(res)}")
            rows.append([f"{gc:.0%}", name, f"{res['mechanics_called_coding']:.3f}", f"{res['mechanics_frame_acc']:.3f}",
                         f"{res['genes_gene_sens']:.3f} / {res['genes_gene_prec']:.3f}",
                         f"{res['accent_called_coding']:.3f}", f"{res['filler_called_coding']:.3f}"])

    cols = ["GC", "target", "mechanics: called coding ↑", "mechanics: frame acc ↑", "mechanics genes sens / prec ↑",
            "accent: called coding ↓", "filler: called coding ↓"]
    lines = ["# Synthetic probe — gene mechanics vs E. coli accent", "",
             "mechanics = ATG + random codons (no E. coli codon preference, no internal stop) + stop.",
             "accent = E. coli codon usage with an in-frame stop every ~18 codons (not a gene).",
             "An organ that learned the mechanics scores high in the ↑ columns and low in the ↓ ones.",
             "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    path = out_dir / "synthetic_probe.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
