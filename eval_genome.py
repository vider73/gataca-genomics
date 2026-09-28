"""Genomics G1, step 3: gene-structure robustness table for organs and baselines.

Targets: organ checkpoints (.pt) and baselines:
  orf       naive rule: ORFs from ATG to stop, >= 300 bp, in 6 frames, greedily kept longest-first
            (overlap < 60 bp). On fragments: a frame with no stop codon across the fragment is coding.
  prodigal  Prodigal (pyrodigal). It trains itself on each (noisy) genome; on fragments it runs in
            metagenomic mode.

Genomes: by default E. coli and B. subtilis; --panel evaluates every genome of data/panel.json.
A genome with role "train" in the panel (and E. coli) is scored on its validation blocks only; a
held-out ("test") species is scored on its whole genome. Conditions: clean; substitutions 1% / 5%; indels 1% (predictions are
mapped back to original positions); 150 bp fragments at random positions (read-like).

Metrics:
  frame acc   on annotated coding bases, fraction with the right strand AND codon position
  coding F1   coding vs non-coding per base
  gene sens / prec   exact stop-codon match (strand + stop coordinate). The organ's genes are read
              off its per-base labels: runs of one strand, split where the codon cycle breaks, >= 90 bp.
              Baselines use their own gene lists.
  + stop snap the organ's genes after one grammar rule: each gene end moves to the nearest stop codon
              in the organ's own reading frame (within 60 bp), as classic gene finders do.
  + grammar decoder   Viterbi over the organ's per-base log-probabilities with a soft gene grammar
              (see grammar_decode): genes open on a start codon, run in codons, close on a stop, have no
              internal stop. Every rule can be broken at a cost, including frameshifts, so the grammar
              bends around sequencing errors instead of breaking. Genes are then read off the decoded
              path like the organ's (split at codon-cycle breaks) and their ends snapped to stops.
              (Reading genes as whole runs of the path merged adjacent operon genes: 0.71 vs 0.91 recall
              on E. coli validation.)

Baseline results (orf, prodigal) are cached: if runs/*/metrics.json already holds them for a genome,
they are reused (--recompute to force), so a panel evaluation of new organs only costs GPU time.

Writes runs/<date>/genomics_g1.md and metrics.json under "eval_genome/<target>/<genome>".
"""

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from numba import njit

from gataca import Progress, genes_to_labels, load_segmenter, mutate, run_dir, tag_stream, update_metrics

STOPS = {"TAA", "TAG", "TGA"}
COMP = str.maketrans("ACGT", "TGCA")
CONDITIONS = [("clean", 0.0, 0.0), ("sub1", 0.01, 0.0), ("sub5", 0.05, 0.0), ("indel1", 0.0, 0.01)]
FRAG_LEN, N_FRAGS = 150, 2000


def to_seq(sym: np.ndarray) -> str:
    return "".join(np.array(list("GATC"))[sym])


def revcomp(s: str) -> str:
    return s.translate(COMP)[::-1]


def stop_anchored_labels(length, genes):
    """Like genes_to_labels, but codon positions counted from the stop end (safe for partial genes)."""
    labels = np.zeros(length, dtype=np.int64)
    for b, e, strand in genes:
        idx = np.arange(max(0, b), min(length, e + 1))
        labels[idx] = ((idx - e + 2) % 3 + 1) if strand == 1 else ((b + 2 - idx) % 3 + 4)
    return labels


# ---------- baselines ----------

def orf_genes(seq: str, min_len=300, max_overlap=60):
    L, cands = len(seq), []
    for strand, s in ((1, seq), (-1, revcomp(seq))):
        for f in range(3):
            codons = [s[i : i + 3] for i in range(f, L - 2, 3)]
            is_stop = np.array([c in STOPS for c in codons])
            is_start = np.array([c == "ATG" for c in codons])
            prev = -1
            for k in np.flatnonzero(is_stop):
                st = np.flatnonzero(is_start[prev + 1 : k])
                if len(st):
                    a = prev + 1 + st[0]
                    b, e = f + 3 * a, f + 3 * k + 2
                    if e - b + 1 >= min_len:
                        cands.append((b, e, 1) if strand == 1 else (L - 1 - e, L - 1 - b, -1))
                prev = k
    covered, kept = np.zeros(L, dtype=bool), []
    for b, e, strand in sorted(cands, key=lambda g: g[0] - g[1]):
        if covered[b : e + 1].sum() < max_overlap:
            kept.append((b, e, strand))
            covered[b : e + 1] = True
    return kept


def orf_fragment_labels(frag: str):
    L = len(frag)
    for strand, s in ((1, frag), (-1, revcomp(frag))):
        for f in range(3):
            if not any(s[i : i + 3] in STOPS for i in range(f, L - 2, 3)):
                idx = np.arange(L)
                if strand == 1:
                    return (idx - f) % 3 + 1
                return (L - 1 - idx - f) % 3 + 4  # position in the reverse-complement string is L-1-idx
    return np.zeros(L, dtype=np.int64)


def prodigal_genes(seq: str, meta=False):
    import pyrodigal

    finder = pyrodigal.GeneFinder(meta=meta, closed=False)
    if not meta:
        finder.train(seq)
    return [(g.begin - 1, g.end - 1, g.strand) for g in finder.find_genes(seq)]


# ---------- organ ----------

def genes_from_labels(labels: np.ndarray, min_len=90):
    """Runs of one strand, split where the codon cycle breaks."""
    genes = []
    fwd_next = {1: 2, 2: 3, 3: 1}
    rev_next = {4: 6, 6: 5, 5: 4}  # along increasing position, reverse codon positions go 3, 2, 1
    start = None
    for i in range(len(labels) + 1):
        cur = labels[i] if i < len(labels) else 0
        prev = labels[i - 1] if i > 0 else 0
        cont = prev > 0 and cur > 0 and (fwd_next.get(prev) == cur or rev_next.get(prev) == cur)
        if start is not None and not cont:
            if i - start >= min_len:
                genes.append((start, i - 1, 1 if prev <= 3 else -1))
            start = None
        if start is None and cur > 0:
            start = i
    return genes


def snap_to_stops(genes, seq: str, labels: np.ndarray, max_shift=60):
    """Move each gene's stop end to the nearest in-frame stop codon, using the organ's own frame."""
    out, L = [], len(seq)
    for b, e, strand in genes:
        if strand == 1:
            third = [i for i in range(e, max(b, e - 6), -1) if labels[i] == 3]  # last base of a codon
            anchor = third[0] if third else e
            cands = [anchor + k for k in range(-max_shift, max_shift + 1, 3)
                     if 2 <= anchor + k < L and seq[anchor + k - 2 : anchor + k + 1] in STOPS]
            if cands:
                e = min(cands, key=lambda p: abs(p - anchor))
        else:
            third = [i for i in range(b, min(e, b + 6)) if labels[i] == 6]  # reverse codon position 3
            anchor = third[0] if third else b
            cands = [anchor + k for k in range(-max_shift, max_shift + 1, 3)
                     if 0 <= anchor + k < L - 2 and revcomp(seq[anchor + k : anchor + k + 3]) in STOPS]
            if cands:
                b = min(cands, key=lambda p: abs(p - anchor))
        out.append((b, e, strand))
    return out


# ---------- grammar decoder ----------

STARTS = ("ATG", "GTG", "TTG")
PENALTIES = {"no_start": 4.0, "no_stop": 4.0, "internal_stop": 6.0, "frameshift": 6.0}


def codon_flags(seq: str):
    """Per position i: forward start codon at i..i+2; forward stop codon ending at i; reverse-strand stop
    codon occupying i..i+2 (the leftmost end of a reverse gene); reverse-strand start codon ending at i
    (its rightmost end)."""
    L = len(seq)
    tri = np.array([seq[i : i + 3] for i in range(L - 2)] + ["NNN", "NNN"])
    fwd_start = np.isin(tri, STARTS)
    rev_stop_begin = np.isin(tri, [revcomp(c) for c in STOPS])
    fwd_stop_end = np.zeros(L, dtype=bool)
    fwd_stop_end[2:] = np.isin(tri[:-2], STOPS)
    rev_start_end = np.zeros(L, dtype=bool)
    rev_start_end[2:] = np.isin(tri[:-2], [revcomp(c) for c in STARTS])
    return fwd_start, fwd_stop_end, rev_stop_begin, rev_start_end


@njit(cache=True)
def _viterbi(logp, fwd_start, fwd_stop_end, rev_stop_begin, rev_start_end, p_start, p_stop, p_internal, p_fs):
    # States = labels: 0 non-coding; 1, 2, 3 forward codon positions; 4, 5, 6 reverse codon positions.
    # Along increasing position a forward gene cycles 1 2 3 and a reverse gene cycles 6 5 4.
    # T[p, s] = cost of moving from state p to state s; codon-dependent entries are filled per position.
    L = logp.shape[0]
    NEG = -1e18
    T = np.full((7, 7), NEG)
    T[0, 0] = 0.0
    T[1, 2] = 0.0
    T[2, 3] = 0.0
    T[6, 5] = 0.0
    T[5, 4] = 0.0
    for a, b in ((1, 1), (1, 3), (2, 2), (2, 1), (3, 3), (3, 2), (6, 6), (6, 4), (5, 5), (5, 6), (4, 4), (4, 5)):
        T[a, b] = -p_fs  # frameshift: repeat a codon position (insertion) or skip one (deletion)
    score = logp[0].copy()
    new = np.empty(7)
    back = np.zeros((L, 7), dtype=np.int8)
    for i in range(1, L):
        T[0, 1] = 0.0 if fwd_start[i] else -p_start
        T[0, 6] = 0.0 if rev_stop_begin[i] else -p_stop
        T[3, 1] = -p_internal if fwd_stop_end[i - 1] else 0.0
        T[3, 0] = 0.0 if fwd_stop_end[i - 1] else -p_stop
        T[4, 6] = -p_internal if rev_stop_begin[i] else 0.0
        T[4, 0] = 0.0 if rev_start_end[i - 1] else -p_start
        for s_ in range(7):
            best, arg = NEG, 0
            for p in range(7):
                v = score[p] + T[p, s_]
                if v > best:
                    best, arg = v, p
            new[s_] = best + logp[i, s_]
            back[i, s_] = arg
        score[:] = new
    path = np.zeros(L, dtype=np.int64)
    path[L - 1] = np.argmax(score)
    for i in range(L - 1, 0, -1):
        path[i - 1] = back[i, path[i]]
    return path


NEXT_LABEL = np.array([0, 2, 3, 1, 6, 4, 5])  # next label inside a gene: forward 1 2 3, reverse 6 5 4 along the read


def frameshift_cost(arg: np.ndarray, lo: float = 2.0, hi: float = PENALTIES["frameshift"]) -> float:
    """Frameshift cost from the sequence's own error level: -log of how often the organ's argmax labels
    break the codon cycle inside coding runs (about one break per indel), clipped to [lo, hi]. Clean DNA
    keeps the default cost; error-laden reads get a cheaper frameshift."""
    a, b = arg[:-1], arg[1:]
    inside = (a > 0) & (b > 0) & ((a > 3) == (b > 3))
    rate = ((b != NEXT_LABEL[a]) & inside).sum() / max(1, inside.sum())
    return float(np.clip(-np.log(max(rate, 1e-9)), lo, hi))


def grammar_decode(logits: torch.Tensor, seq: str, penalties=PENALTIES, weight: float = 1.0,
                   adaptive: bool = False) -> np.ndarray:
    """Most likely per-base labels under the soft gene grammar, from the organ's logits [L, 7].
    weight < 1 softens the organ's (very confident) log-probabilities relative to the grammar costs.
    adaptive: the frameshift cost follows the sequence's own error level (frameshift_cost). Off by default:
    +1.4 pt frame acc on 18%-error nanopore reads, but -0.2 to -0.6 pt genes under 5% subs / 1% indels
    (runs/2026-09-28, eval_nanopore_fsauto.log, genomics_fsauto.md)."""
    logp = weight * torch.log_softmax(logits.float(), -1).cpu().numpy().astype(np.float64)
    fs = frameshift_cost(logp.argmax(-1)) if adaptive else penalties["frameshift"]
    return _viterbi(logp, *codon_flags(seq), penalties["no_start"], penalties["no_stop"],
                    penalties["internal_stop"], fs)


# ---------- scoring ----------

def base_scores(pred, gold, mask):
    p, g = pred[mask], gold[mask]
    pc, gc = p > 0, g > 0
    tp = (pc & gc).sum()
    prec, rec = tp / max(1, pc.sum()), tp / max(1, gc.sum())
    return {"frame_acc": float((p[gc] == g[gc]).mean()), "coding_f1": float(2 * prec * rec / max(1e-9, prec + rec)),
            "acc": float((p == g).mean())}


def gene_scores(pred_genes, true_genes, mask):
    stop = lambda g: (g[2], g[1] if g[2] == 1 else g[0])
    t = {stop(g) for g in true_genes if mask[stop(g)[1]]}
    p = {stop(g) for g in pred_genes if mask[stop(g)[1]]}
    hit = len(t & p)
    return {"gene_sens": hit / max(1, len(t)), "gene_prec": hit / max(1, len(p)), "n_true": len(t), "n_pred": len(p)}


def map_genes_to_original(genes, orig_idx: np.ndarray):
    """Gene coordinates on a noisy sequence -> original coordinates (ends snap to the nearest kept base inside)."""
    kept = np.flatnonzero(orig_idx >= 0)
    out = []
    for a, b, st in genes:
        lo = kept[np.searchsorted(kept, a)] if np.searchsorted(kept, a) < len(kept) else None
        hi_i = np.searchsorted(kept, b, side="right") - 1
        if lo is None or hi_i < 0 or kept[hi_i] < lo:
            continue
        out.append((int(orig_idx[lo]), int(orig_idx[kept[hi_i]]), st))
    return out


def back_to_original(pred_noisy: np.ndarray, orig_idx: np.ndarray, L: int):
    """Per-base predictions on a noisy sequence -> original coordinates (deleted bases: forward-filled)."""
    out = np.full(L, -1, dtype=np.int64)
    keep = orig_idx >= 0
    out[orig_idx[keep]] = pred_noisy[keep]
    observed = out >= 0
    fill = np.maximum.accumulate(np.where(observed, np.arange(L), 0))
    return np.where(observed, out, out[fill].clip(min=0)), observed


def evaluate(target, sym, true_genes, region, device, seed):
    L = len(sym)
    gold = genes_to_labels(L, true_genes)
    res = {}
    model = None if target in ("orf", "prodigal") else load_segmenter(Path(target), device)[0]
    for name, sub, indel in CONDITIONS:
        rng = np.random.default_rng(seed)
        noisy, idx = mutate(sym, sub, indel, rng)
        genes = None
        if model is not None:
            logits = tag_stream(model, torch.from_numpy(noisy.astype(np.int64)).to(device))
            pred_n = logits.argmax(-1).cpu().numpy()
            noisy_seq = to_seq(noisy)
            dec_n = grammar_decode(logits, noisy_seq)
            dec, dec_obs = back_to_original(dec_n, idx, L)
            # genes are read on the noisy sequence the decoder saw (split at codon-cycle breaks, ends
            # snapped to in-frame stops), then mapped to original coordinates
            dec_genes = map_genes_to_original(snap_to_stops(genes_from_labels(dec_n), noisy_seq, dec_n), idx)
        else:
            s = to_seq(noisy)
            genes = orf_genes(s) if target == "orf" else prodigal_genes(s)
            pred_n = stop_anchored_labels(len(noisy), genes)
        pred, observed = back_to_original(pred_n, idx, L)
        r = base_scores(pred, gold, region & observed)
        if model is not None:
            r["frame_acc_dec"] = base_scores(dec, gold, region & dec_obs)["frame_acc"]
            r |= {f"{k}_dec": v for k, v in gene_scores(dec_genes, true_genes, region).items()}
        if indel == 0:
            if genes is None:  # organ
                genes = genes_from_labels(pred)
                snapped = snap_to_stops(genes, to_seq(noisy), pred)
                r |= {f"{k}_snap": v for k, v in gene_scores(snapped, true_genes, region).items()}
            r |= gene_scores(genes, true_genes, region)
        elif model is not None:
            r |= gene_scores(genes_from_labels(pred), true_genes, region)
        res[name] = r

    rng = np.random.default_rng(seed)
    starts = rng.choice(np.flatnonzero(region[: L - FRAG_LEN] & region[FRAG_LEN:]), N_FRAGS, replace=False)
    preds, golds = [], []
    for s in starts:
        frag = sym[s : s + FRAG_LEN]
        if model is not None:
            p = tag_stream(model, torch.from_numpy(frag.astype(np.int64)).to(device)).argmax(-1).cpu().numpy()
        elif target == "orf":
            p = orf_fragment_labels(to_seq(frag))
        else:
            p = stop_anchored_labels(FRAG_LEN, prodigal_genes(to_seq(frag), meta=True))
        preds.append(p)
        golds.append(gold[s : s + FRAG_LEN])
    preds, golds = np.concatenate(preds), np.concatenate(golds)
    res["frag150"] = base_scores(preds, golds, np.ones(len(preds), dtype=bool))
    return res


def cached_baseline(name: str, genome: str):
    for mpath in sorted(Path("runs").glob("*/metrics.json"), reverse=True):
        found = json.loads(mpath.read_text()).get(f"eval_genome/{name}/{genome}")
        if found and "frag150" in found:
            return found
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("targets", nargs="+", help="organ checkpoints and/or orf, prodigal")
    p.add_argument("--genomes", nargs="+", default=["ecoli", "bsubtilis"])
    p.add_argument("--panel", action="store_true", help="evaluate every genome of data/panel.json")
    p.add_argument("--out", default="genomics_g1.md")
    p.add_argument("--recompute", action="store_true", help="do not reuse cached baseline results")
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    out_dir = run_dir(args.runs_dir)
    rows = []
    panel_path = Path("data/panel.json")
    panel = json.loads(panel_path.read_text()) if panel_path.exists() else {}
    genomes = list(panel) if args.panel else args.genomes
    progress = Progress(args.runs_dir, f"eval_{Path(args.out).stem}", len(genomes) * len(args.targets), "eval_genome")
    n_done = 0
    for genome in genomes:
        d = Path("data") / f"genome_{genome}"
        sym, genes = np.load(d / "symbols.npy"), [tuple(g) for g in np.load(d / "genes.npy")]
        split = np.load(d / "split.npy")
        # Genomes whose train blocks may be used for training: score validation blocks only.
        trainable = genome == "ecoli" or panel.get(genome, {}).get("role") == "train"
        region = split == 1 if trainable else np.ones(len(sym), dtype=bool)
        label = f"{genome} (validation blocks)" if trainable else f"{genome} (whole genome, held-out species)"
        for target in args.targets:
            name = target if target in ("orf", "prodigal") else Path(target).stem
            res = cached_baseline(name, genome) if name in ("orf", "prodigal") and not args.recompute else None
            if res is None:
                res = evaluate(target, sym, genes, region, device, args.seed)
                update_metrics(out_dir, f"eval_genome/{name}/{genome}", res)
            n_done += 1
            progress.update(n_done, force=True)
            print(genome, name, json.dumps(res["clean"]))
            c = res["clean"]
            g = lambda k, m: f"{res[k][m]:.3f}" if m in res[k] else "—"
            snap = f"{c['gene_sens_snap']:.3f} / {c['gene_prec_snap']:.3f}" if "gene_sens_snap" in c else "—"
            dec = lambda k: f"{res[k]['gene_sens_dec']:.3f} / {res[k]['gene_prec_dec']:.3f}" if "gene_sens_dec" in res[k] else "—"
            rows.append([label, name, f"{c['frame_acc']:.3f}", f"{c['coding_f1']:.3f}",
                         f"{c['gene_sens']:.3f} / {c['gene_prec']:.3f}", snap, dec("clean"), dec("sub5"), dec("indel1"),
                         g("sub1", "frame_acc"), g("sub5", "frame_acc"),
                         f"{res['sub5']['gene_sens']:.3f} / {res['sub5']['gene_prec']:.3f}",
                         g("indel1", "frame_acc"), g("indel1", "gene_sens"), g("frag150", "frame_acc")])

    progress.done()
    cols = ["genome", "target", "frame acc", "coding F1", "genes sens / prec", "genes + stop snap",
            "genes grammar decoder", "decoder sub 5%", "decoder indel 1%", "frame acc sub 1%",
            "frame acc sub 5%", "genes sens / prec sub 5%", "frame acc indel 1%", "gene sens indel 1%",
            "frame acc 150 bp fragments"]
    lines = ["# Genomics G1 — gene structure from raw bases", "",
             "Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.",
             "Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.",
             "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    path = out_dir / args.out
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
