"""Genomics G1, real errors, step 2: organs vs Prodigal on real nanopore reads.

Reads come from prepare_nanopore.py (reference-oriented, trimmed to the aligned part, each base with
its reference position or -1 if inserted by the sequencer). Every target sees each read on its own,
as a gene finder sees reads before assembly:
  organ checkpoints   argmax labels, and the grammar decoder (Viterbi + codon-cycle split + stop snap)
  prodigal            Prodigal in metagenomic mode on each read
  orf                 the naive ORF rule
Control rows ("clean"): the same reference stretch without sequencing errors, to separate the cost
of the errors from the cost of short, partial genes.

Metrics, over all reads:
  frame acc   read bases that came from annotated coding bases, predicted with the right strand
              and codon position (inserted bases are not scored)
  coding F1   coding vs non-coding on the same bases
  gene sens / prec   reference genes lying fully inside a read, found with the exact stop codon
              (predicted stops are mapped back to reference coordinates)

Writes runs/<date>/nanopore_<genome>.md and metrics.json under "eval_nanopore/<run>/<target>".
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from eval_genome import (genes_from_labels, grammar_decode, orf_genes, prodigal_genes, snap_to_stops,
                         stop_anchored_labels, to_seq)
from gataca import Progress, genes_to_labels, load_segmenter, run_dir, tag_stream, update_metrics


class Tally:
    def __init__(self):
        self.frame_ok = self.coding = self.tp = self.pc = self.gc = 0
        self.g_true = self.g_found = self.g_pred = self.g_pred_ok = 0

    def bases(self, pred, gold):
        m = gold >= 0
        pred, gold = pred[m], gold[m]
        gcod, pcod = gold > 0, pred > 0
        self.frame_ok += int((pred[gcod] == gold[gcod]).sum())
        self.coding += int(gcod.sum())
        self.tp += int((gcod & pcod).sum())
        self.pc += int(pcod.sum())
        self.gc += int(gcod.sum())

    def genes(self, pred_stops: set, true_stops: set, span):
        lo, hi = span
        pred_in = {s for s in pred_stops if lo <= s[1] <= hi}
        self.g_true += len(true_stops)
        self.g_found += len(true_stops & pred_in)
        self.g_pred += len(pred_in)
        self.g_pred_ok += len(pred_in & true_stops)

    def result(self):
        p, r = self.tp / max(1, self.pc), self.tp / max(1, self.gc)
        return {"frame_acc": self.frame_ok / max(1, self.coding), "coding_f1": 2 * p * r / max(1e-9, p + r),
                "gene_sens": self.g_found / max(1, self.g_true), "gene_prec": self.g_pred_ok / max(1, self.g_pred),
                "genes_true": self.g_true}


def stops_to_ref(genes, refpos):
    """Predicted genes on a read -> set of (strand, reference stop coordinate)."""
    kept = np.flatnonzero(refpos >= 0)
    out = set()
    for a, b, st in genes:
        k = b if st == 1 else a
        j = kept[np.clip(np.searchsorted(kept, k), 0, len(kept) - 1)]
        out.add((st, int(refpos[j])))
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("targets", nargs="+", help="organ checkpoints and/or prodigal, orf")
    p.add_argument("--runs", nargs="+", required=True, help="prepared nanopore runs (data/nanopore/<run>)")
    p.add_argument("--genome", default="hvolcanii")
    p.add_argument("--max-bases", type=float, default=4e6, help="random reads up to this many bases per run")
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    gdir = Path("data") / f"genome_{args.genome}"
    ref_sym = np.load(gdir / "symbols.npy")
    ref_genes = [tuple(int(x) for x in g) for g in np.load(gdir / "genes.npy")]
    ref_labels = genes_to_labels(len(ref_sym), ref_genes)
    stop_of = lambda g: (g[2], g[1] if g[2] == 1 else g[0])
    models = {t: load_segmenter(Path(t), device)[0] for t in args.targets if t not in ("prodigal", "orf")}
    out_dir = run_dir(args.runs_dir)
    rows = []

    for run in args.runs:
        d = Path("data/nanopore") / run
        sym, refpos, offsets = np.load(d / "symbols.npy"), np.load(d / "refpos.npy"), np.load(d / "offsets.npy")
        meta = json.loads((d / "meta.json").read_text())
        order = np.random.default_rng(args.seed).permutation(len(offsets) - 1)
        picked, total = [], 0
        for i in order:
            picked.append(i)
            total += offsets[i + 1] - offsets[i]
            if total >= args.max_bases:
                break
        tallies = {}
        progress = Progress(args.runs_dir, f"nanopore_{run}", len(picked), "eval_nanopore")
        for n_read, i in enumerate(picked):
            rs, rp = sym[offsets[i] : offsets[i + 1]], refpos[offsets[i] : offsets[i + 1]]
            lo, hi = int(rp[rp >= 0].min()), int(rp[rp >= 0].max())
            true_stops = {stop_of(g) for g in ref_genes if g[0] >= lo and g[1] <= hi}
            gold = np.where(rp >= 0, ref_labels[np.maximum(rp, 0)], -1)
            clean_sym = ref_sym[lo : hi + 1]
            clean_rp = np.arange(lo, hi + 1)
            clean_gold = ref_labels[lo : hi + 1]
            for kind, s_, rp_, gold_ in (("reads", rs, rp, gold), ("clean", clean_sym, clean_rp, clean_gold)):
                seq = to_seq(s_)
                for t in args.targets:
                    name = t if t in ("prodigal", "orf") else Path(t).stem
                    if t in models:
                        logits = tag_stream(models[t], torch.from_numpy(s_.astype(np.int64)).to(device))
                        arg = logits.argmax(-1).cpu().numpy()
                        dec = grammar_decode(logits, seq)
                        variants = {name: (arg, snap_to_stops(genes_from_labels(arg), seq, arg)),
                                    f"{name} + grammar decoder": (dec, snap_to_stops(genes_from_labels(dec), seq, dec))}
                    else:
                        genes = prodigal_genes(seq, meta=True) if t == "prodigal" else orf_genes(seq)
                        variants = {name: (stop_anchored_labels(len(s_), genes), genes)}
                    for vname, (labels, genes) in variants.items():
                        tal = tallies.setdefault((kind, vname), Tally())
                        tal.bases(labels, gold_)
                        tal.genes(stops_to_ref(genes, rp_), true_stops, (lo, hi))
            progress.update(n_read + 1)
            if n_read % 50 == 0:
                print(f"{run}: {n_read + 1}/{len(picked)} reads", flush=True)
        progress.done()
        for (kind, vname), tal in tallies.items():
            res = tal.result()
            update_metrics(out_dir, f"eval_nanopore/{run}/{kind}/{vname}", res)
            rows.append([run, f"{meta['identity']:.1%}", kind, vname, f"{res['frame_acc']:.3f}", f"{res['coding_f1']:.3f}",
                         f"{res['gene_sens']:.3f} / {res['gene_prec']:.3f}", str(res["genes_true"])])
        print(f"{run}: {len(picked)} reads, {total:,} bases scored", flush=True)

    cols = ["run", "read identity", "input", "target", "frame acc", "coding F1", "genes sens / prec (exact stop)", "genes in reads"]
    lines = [f"# Real nanopore reads — {args.genome} (held-out species)", "",
             "reads = the real reads; clean = the same reference stretches without sequencing errors.",
             "Each read is processed on its own. Prodigal runs in metagenomic mode.", "",
             "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(r) + " |" for r in sorted(rows, key=lambda r: (r[0], r[2] != "reads", r[3]))]
    path = out_dir / f"nanopore_{args.genome}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
