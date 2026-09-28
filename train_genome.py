"""Genomics G1, step 2: train an organ to read gene structure from raw bases.

Per base, 7 classes: non-coding, or coding on the forward/reverse strand at codon position 1/2/3.
Windows are drawn only from train blocks. Each window is read on a random strand (reverse-complement
augmentation). --noise aug adds sequencing-style noise per window: substitutions at a rate drawn
from [0, --sub-max] and insertions/deletions at a rate drawn from [0, --indel-max]. Inserted bases
carry no label, so the organ is scored on recovering the original annotation despite frameshifts.
--noise ont uses gataca.mutate_nanopore instead: a total error rate drawn from [0, --err-max] per window,
indel-heavy, homopolymer-biased and bursty (a published nanopore error profile, not fit to our reads).
--err-dist mix skews that rate to low values: with probability 1 - --err-tail it is exponential with
mean --err-mean (capped at --err-max), otherwise uniform in [0, --err-max].
--ont-sub-max adds uniform substitutions at a rate drawn from [0, --ont-sub-max] on top of the nanopore errors.
--init starts from an existing checkpoint (fine-tuning).

Several genomes: --panel trains on every "train" genome of data/panel.json (or --genomes a b c);
windows are drawn from each genome in proportion to its number of train windows.
--synthetic-frac f replaces a fraction f of every batch with synthetic DNA (gataca.synthetic_dna):
genes with pure gene grammar at random GC (25-75%) and decoys with a real species' codon usage but
no gene grammar. It rewards the grammar and punishes relying on a species' accent.

Logged to runs/<date>/metrics.json under "train_genome/<run>": per-base accuracy, coding F1 and
frame accuracy (correct strand + codon position on coding bases) on validation windows (the mean
over genomes and per genome), plus the synthetic probe: the fraction of grammar-only genes called
coding (mech_coding, higher is better) and of accent-only decoys called coding (accent_coding, lower).
"""

import argparse
import datetime
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from gataca import (GENE_CLASSES, Progress, Segmenter, codon_usage, load_segmenter, mutate, mutate_nanopore,
                    reverse_complement, run_dir, save_model, synthetic_dna, tag_stream, update_metrics)

IGNORE = -100


def valid_starts(split: np.ndarray, which: int, W: int) -> np.ndarray:
    """Window starts whose W bases all belong to split `which`."""
    ok = np.concatenate([[0], np.cumsum(split == which)])
    return np.flatnonzero(ok[W:] - ok[:-W] == W)


def make_batch(sym, lab, starts, W, rng, noise, sub_max, indel_max, err_max=0.0):
    """Windows of one genome."""
    return make_batch_items([(sym, lab, s) for s in starts], W, rng, noise, sub_max, indel_max, err_max)


def ont_rate(rng, err_max, dist="uniform", err_mean=0.04, err_tail=0.15):
    """Total nanopore error rate for one window."""
    if dist == "mix" and rng.random() >= err_tail:
        return min(rng.exponential(err_mean), err_max)
    return rng.random() * err_max


def make_batch_items(items, W, rng, noise, sub_max, indel_max, err_max=0.0, err_dist="uniform", err_mean=0.04,
                     err_tail=0.15, ont_sub_max=0.0):
    """items: (symbols, labels, start) triples, possibly from different genomes.
    noise: False, True (uniform subs + indels), "ont" (nanopore, rate up to err_max) or "fixed_ont" (rate err_max)."""
    xs, ys = [], []
    for sym, lab, s in items:
        x, y = sym[s : s + W + 64], lab[s : s + W + 64].astype(np.int64)  # spare bases for deletions
        if noise == "ont":
            x, idx = mutate_nanopore(x, ont_rate(rng, err_max, err_dist, err_mean, err_tail), rng)
            if ont_sub_max > 0:
                x = mutate(x, rng.random() * ont_sub_max, 0.0, rng)[0]
        elif noise == "fixed_ont":
            x, idx = mutate_nanopore(x, err_max, rng)
        elif noise:
            x, idx = mutate(x, rng.random() * sub_max, rng.random() * indel_max, rng)
        if noise:
            y = np.where(idx >= 0, y[np.maximum(idx, 0)], IGNORE)
        x, y = x[:W], y[:W]
        if rng.random() < 0.5:
            x, y = reverse_complement(x, y)
        if len(x) < W:
            x = np.pad(x, (0, W - len(x)))
            y = np.pad(y, (0, W - len(y)), constant_values=IGNORE)
        xs.append(x)
        ys.append(y)
    return torch.from_numpy(np.stack(xs).astype(np.int64)), torch.from_numpy(np.stack(ys))


def base_metrics(pred: torch.Tensor, gold: torch.Tensor) -> dict:
    m = gold != IGNORE
    pred, gold = pred[m], gold[m]
    pc, gc = pred > 0, gold > 0
    tp = (pc & gc).sum().item()
    p, r = tp / max(1, pc.sum().item()), tp / max(1, gc.sum().item())
    return {"acc": (pred == gold).float().mean().item(), "coding_f1": 2 * p * r / max(1e-9, p + r),
            "frame_acc": (pred[gc] == gold[gc]).float().mean().item()}


class Source:
    """One genome with the window starts usable for training and validation."""

    def __init__(self, name, sym, lab, split, W):
        self.name, self.sym, self.lab = name, sym, lab
        self.train_starts = valid_starts(split, 0, W + 64)
        self.val_starts = valid_starts(split, 1, W + 64)


def load_source(data_dir: Path, W: int) -> Source:
    return Source(data_dir.name.removeprefix("genome_"), np.load(data_dir / "symbols.npy"),
                  np.load(data_dir / "labels.npy"), np.load(data_dir / "split.npy"), W)


def synthetic_pool(usages, gcs, segments, seed):
    """Concatenated synthetic genomes over a GC range; decoys use the codon usage of a random real genome.
    Returns (symbols, labels, kind) with kind per base: 0 filler, 1 grammar-only gene, 2 accent-only decoy."""
    rng = np.random.default_rng(seed)
    syms, labs, kinds = [], [], []
    for gc in gcs:
        sym, lab, _, segs = synthetic_dna(gc, segments, rng, usages[rng.integers(len(usages))])
        kind = np.zeros(len(sym), dtype=np.uint8)
        for a, b, k in segs:
            kind[a:b] = {"filler": 0, "mechanics": 1, "accent": 2}[k]
        syms.append(sym)
        labs.append(lab)
        kinds.append(kind)
    return np.concatenate(syms), np.concatenate(labs), np.concatenate(kinds)


@torch.no_grad()
def probe(model, pool, device) -> dict:
    sym, _, kind = pool
    pred = tag_stream(model, torch.from_numpy(sym.astype(np.int64)).to(device)).argmax(-1).cpu().numpy()
    model.train()
    return {"mech_coding": float((pred[kind == 1] > 0).mean()), "accent_coding": float((pred[kind == 2] > 0).mean())}


@torch.no_grad()
def evaluate(model, batch, device):
    model.eval()
    x, y = batch
    with torch.autocast(device_type=device, dtype=torch.bfloat16, enabled=device == "cuda"):
        pred = model(x.to(device)).float().argmax(-1)
    model.train()
    return base_metrics(pred.cpu(), y)


def lr_at(step, total, warmup, peak):
    if step < warmup:
        return peak * (step + 1) / warmup
    return peak * 0.5 * (1 + math.cos(math.pi * (step - warmup) / max(1, total - warmup)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", type=Path, default=Path("data/genome_ecoli"))
    p.add_argument("--genomes", nargs="+", default=None, help="genome names (data/genome_<name>) to train on")
    p.add_argument("--panel", action="store_true", help="train on every 'train' genome of data/panel.json")
    p.add_argument("--synthetic-frac", type=float, default=0.0, help="fraction of each batch from synthetic DNA")
    p.add_argument("--synthetic-segments", type=int, default=300, help="segments per GC value in the synthetic pool")
    p.add_argument("--runs-dir", type=Path, default=Path("runs"))
    p.add_argument("--run-name", default=None)
    p.add_argument("--steps", type=int, default=6000)
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--window", type=int, default=1024)
    p.add_argument("--lr", type=float, default=5e-4)
    p.add_argument("--warmup", type=int, default=300)
    p.add_argument("--weight-decay", type=float, default=0.05)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--d-model", type=int, default=256)
    p.add_argument("--layers", type=int, default=4)
    p.add_argument("--heads", type=int, default=8)
    p.add_argument("--conv-layers", type=int, default=6, help="dilated conv stem before attention (0 = none)")
    p.add_argument("--noise", choices=["none", "aug", "ont"], default="none")
    p.add_argument("--err-max", type=float, default=0.15, help="--noise ont: max total error rate per window")
    p.add_argument("--err-dist", choices=["uniform", "mix"], default="uniform", help="--noise ont: rate distribution")
    p.add_argument("--err-mean", type=float, default=0.04, help="--err-dist mix: mean of the exponential part")
    p.add_argument("--err-tail", type=float, default=0.15, help="--err-dist mix: fraction of windows uniform in [0, max]")
    p.add_argument("--ont-sub-max", type=float, default=0.0, help="--noise ont: extra uniform subs, rate in [0, max]")
    p.add_argument("--init", type=Path, default=None, help="start from this checkpoint")
    p.add_argument("--sub-max", type=float, default=0.05)
    p.add_argument("--indel-max", type=float, default=0.02)
    p.add_argument("--eval-every", type=int, default=500)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    torch.manual_seed(args.seed)
    rng = np.random.default_rng(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    run_name = args.run_name or datetime.datetime.now().strftime("%H%M%S")
    out_dir = run_dir(args.runs_dir)
    W = args.window

    if args.panel:
        panel = json.loads(Path("data/panel.json").read_text())
        names = [n for n, v in panel.items() if v["role"] == "train"]
    else:
        names = args.genomes
    dirs = [Path("data") / f"genome_{n}" for n in names] if names else [args.data]
    sources = [load_source(d, W) for d in dirs]
    weights = np.array([len(src.train_starts) for src in sources], dtype=float)
    weights /= weights.sum()

    # Validation: 128 windows for a single genome (as before), 32 per genome otherwise.
    vrng = np.random.default_rng(1234)
    n_val = 128 if len(sources) == 1 else 32
    val_sets = {}
    for src in sources:
        val_sets[src.name] = (
            make_batch(src.sym, src.lab, vrng.choice(src.val_starts, n_val, replace=False), W, vrng, False, 0, 0),
            make_batch(src.sym, src.lab, vrng.choice(src.val_starts, n_val, replace=False), W, vrng, True, 0.05, 0.02),
            make_batch(src.sym, src.lab, vrng.choice(src.val_starts, n_val, replace=False), W, vrng, "fixed_ont", 0, 0, 0.08))

    # Synthetic data: a training pool, and a separate probe pool (other seed) to measure grammar vs accent.
    usages = [codon_usage(np.load(d / "symbols.npy"), [tuple(g) for g in np.load(d / "genes.npy")],
                          np.load(d / "split.npy") == 0) for d in dirs]
    synth = None
    if args.synthetic_frac > 0:
        synth = synthetic_pool(usages, np.linspace(0.25, 0.75, 11), args.synthetic_segments, args.seed + 100)
        synth_starts = np.arange(len(synth[0]) - W - 64)
        print(f"synthetic pool: {len(synth[0]):,} bases")
    probe_pool = synthetic_pool(usages, [0.35, 0.5, 0.65], 100, 999)
    train_windows = int(sum(len(src.train_starts) for src in sources))

    if args.init:
        model = load_segmenter(args.init, device)[0]
        model.train()
    else:
        model = Segmenter(args.d_model, args.layers, args.heads, dropout=args.dropout, window=W,
                          n_out=GENE_CLASSES, conv_layers=args.conv_layers).to(device)
    n_params = sum(q.numel() for q in model.parameters())
    print(f"organ params: {n_params:,}  device: {device}  run: {run_name}  genomes: {[s.name for s in sources]}  "
          f"train windows: {train_windows:,}  synthetic frac: {args.synthetic_frac}")
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    history, running, t0 = [], 0.0, time.time()
    progress = Progress(args.runs_dir, run_name, args.steps, "train_genome")
    for step in range(args.steps):
        for group in opt.param_groups:
            group["lr"] = lr_at(step, args.steps, args.warmup, args.lr)
        n_syn = int(round(args.synthetic_frac * args.batch)) if synth is not None else 0
        picks = rng.choice(len(sources), args.batch - n_syn, p=weights)
        items = [(sources[i].sym, sources[i].lab, rng.choice(sources[i].train_starts)) for i in picks]
        items += [(synth[0], synth[1], rng.choice(synth_starts)) for _ in range(n_syn)]
        noise = {"none": False, "aug": True, "ont": "ont"}[args.noise]
        x, y = make_batch_items(items, W, rng, noise, args.sub_max, args.indel_max, args.err_max, args.err_dist,
                                args.err_mean, args.err_tail, args.ont_sub_max)
        with torch.autocast(device_type=device, dtype=torch.bfloat16, enabled=device == "cuda"):
            logits = model(x.to(device))
        loss = F.cross_entropy(logits.float().reshape(-1, GENE_CLASSES), y.to(device).reshape(-1), ignore_index=IGNORE)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        running += loss.item()
        progress.update(step + 1, loss=loss.item())

        if (step + 1) % args.eval_every == 0 or step + 1 == args.steps:
            m = {"step": step + 1, "train_loss": running / args.eval_every, "elapsed_s": round(time.time() - t0, 1)}
            per = {n: [evaluate(model, b, device) for b in bs] for n, bs in val_sets.items()}
            for k in ("acc", "coding_f1", "frame_acc"):
                m[f"{k}_clean"] = float(np.mean([v[0][k] for v in per.values()]))
                m[f"{k}_noisy"] = float(np.mean([v[1][k] for v in per.values()]))
                m[f"{k}_ont8"] = float(np.mean([v[2][k] for v in per.values()]))
            if len(per) > 1:
                m["frame_acc_clean_per_genome"] = {n: v[0]["frame_acc"] for n, v in per.items()}
            m |= probe(model, probe_pool, device)
            running = 0.0
            history.append(m)
            print(f"step {m['step']:>6}  loss {m['train_loss']:.4f}  clean acc {m['acc_clean']:.4f} "
                  f"coding F1 {m['coding_f1_clean']:.4f} frame {m['frame_acc_clean']:.4f}  |  "
                  f"noisy (5% sub, 2% indel) frame {m['frame_acc_noisy']:.4f}  ont 8% {m['frame_acc_ont8']:.4f}  |  grammar genes coding "
                  f"{m['mech_coding']:.3f}  accent decoys coding {m['accent_coding']:.3f}  ({m['elapsed_s']}s)", flush=True)
            progress.update(step + 1, force=True, frame_acc=m["frame_acc_clean"], frame_acc_noisy=m["frame_acc_noisy"], frame_acc_ont8=m["frame_acc_ont8"],
                            mech_coding=m["mech_coding"], accent_coding=m["accent_coding"])

    ckpt = out_dir / f"genome_{run_name}.pt"
    save_model(ckpt, model, {"args": {k: str(v) for k, v in vars(args).items()},
                             "trained_on": [s.name for s in sources]})
    result = {"checkpoint": str(ckpt), "params": n_params,
              "args": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
              "trained_on": [s.name for s in sources],
              "final": history[-1], "history": history}
    print(json.dumps(history[-1], indent=2))
    print(f"wrote {ckpt} and {update_metrics(out_dir, f'train_genome/{run_name}', result)}")
    progress.done()


if __name__ == "__main__":
    main()
