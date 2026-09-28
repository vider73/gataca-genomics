"""Shared pieces: the organ model, data loading and run logging."""

import datetime
import json
import os
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

MAX_SYMBOLS = 64  # 16 bytes * 4 symbols per byte
N_SYMBOLS = 4  # G, A, T, C


def bytes_to_symbols_np(data: np.ndarray) -> np.ndarray:
    """uint8 bytes [N] -> uint8 symbols [4N], most significant pair first (G=0, A=1, T=2, C=3)."""
    return np.stack([(data >> 6) & 3, (data >> 4) & 3, (data >> 2) & 3, data & 3], axis=1).reshape(-1).astype(np.uint8)


def add_symbol_noise(symbols: torch.Tensor, p: float, generator=None) -> torch.Tensor:
    """Substitute each symbol with probability p by one of the 3 other symbols."""
    if p <= 0:
        return symbols
    flip = torch.rand(symbols.shape, device=symbols.device, generator=generator) < p
    shift = torch.randint(1, N_SYMBOLS, symbols.shape, device=symbols.device, generator=generator)
    return torch.where(flip, (symbols + shift) % N_SYMBOLS, symbols)


def mutate(symbols: np.ndarray, sub_rate: float, indel_rate: float, rng: np.random.Generator):
    """Sequencing-style noise on a 1-D symbol array.

    Substitutions at sub_rate (to one of the 3 other symbols); deletions and insertions of a random
    symbol at indel_rate / 2 each. Returns (noisy symbols, orig_idx) where orig_idx[j] is the original
    position of noisy symbol j, or -1 for an inserted symbol.
    """
    s = symbols.astype(np.int64)
    if sub_rate > 0:
        flip = rng.random(len(s)) < sub_rate
        s = np.where(flip, (s + rng.integers(1, N_SYMBOLS, len(s))) % N_SYMBOLS, s)
    idx = np.arange(len(s))
    if indel_rate > 0:
        keep = rng.random(len(s)) >= indel_rate / 2
        s, idx = s[keep], idx[keep]
        ins = np.flatnonzero(rng.random(len(s)) < indel_rate / 2)
        s = np.insert(s, ins + 1, rng.integers(0, N_SYMBOLS, len(ins)))
        idx = np.insert(idx, ins + 1, -1)
    return s.astype(np.uint8), idx


def mutate_nanopore(symbols: np.ndarray, rate: float, rng: np.random.Generator, mix=(0.35, 0.25, 0.40),
                    mix_conc=20.0, hp_boost=4.0, burst_sigma=0.7, burst_len=200):
    """Nanopore-style sequencing errors, from published error profiles (not fit to any evaluation read set).

    rate is the total error rate per base. Its split into substitutions / insertions / deletions is drawn
    around `mix` (Dirichlet with concentration mix_conc); nanopore errors are indel-heavy with deletions
    most common. Indels are hp_boost times more likely inside homopolymers (runs of >= 3 equal bases),
    where an insertion repeats the run's base: the sequencer misjudges the run length. Errors come in
    bursts: the local rate is scaled by a log-normal factor (mean 1) that changes every ~burst_len bases.
    Returns (noisy symbols, orig_idx) like mutate(): orig_idx is -1 for inserted symbols.
    """
    s = symbols.astype(np.int64)
    n = len(s)
    if rate <= 0 or n == 0:
        return s.astype(np.uint8), np.arange(n)
    p_sub, p_ins, p_del = rate * rng.dirichlet(np.asarray(mix) * mix_conc)
    mult = rng.lognormal(-burst_sigma**2 / 2, burst_sigma, n // burst_len + 2)
    field = np.repeat(mult, burst_len)[rng.integers(burst_len) :][:n]
    new_run = np.r_[True, s[1:] != s[:-1]]
    run_id = np.cumsum(new_run) - 1
    hp = np.bincount(run_id)[run_id] >= 3
    w = field * np.where(hp, hp_boost, 1.0)
    w *= field.mean() / w.mean()  # homopolymers move indels around, not the overall rate
    flip = rng.random(n) < np.minimum(p_sub * field, 0.75)
    s = np.where(flip, (s + rng.integers(1, N_SYMBOLS, n)) % N_SYMBOLS, s)
    keep = rng.random(n) >= np.minimum(p_del * w, 0.75)
    ins = rng.random(n) < np.minimum(p_ins * w, 0.75)
    ins_base = np.where(hp, s, rng.integers(0, N_SYMBOLS, n))
    vals = np.stack([s, ins_base], 1).reshape(-1)
    idx = np.stack([np.arange(n), np.full(n, -1)], 1).reshape(-1)
    sel = np.stack([keep, ins], 1).reshape(-1)
    return vals[sel].astype(np.uint8), idx[sel]


# Gene-structure classes: 0 non-coding, 1..3 forward codon position 1..3, 4..6 reverse codon position 1..3.
GENE_CLASSES = 7
REVCOMP_LABEL = np.array([0, 4, 5, 6, 1, 2, 3], dtype=np.int64)


def reverse_complement(symbols: np.ndarray, labels: np.ndarray):
    """Read the other strand: complement (G<->C, A<->T is 3 - s in the G/A/T/C mapping), reverse, swap strands."""
    return (3 - symbols[::-1]).astype(symbols.dtype), np.where(labels[::-1] < 0, labels[::-1], REVCOMP_LABEL[np.maximum(labels[::-1], 0)])


def genes_to_labels(length: int, genes) -> np.ndarray:
    """(start, end, strand) 0-based inclusive -> per-base gene-structure labels (later genes overwrite)."""
    labels = np.zeros(length, dtype=np.int64)
    for start, end, strand in genes:
        idx = np.arange(max(0, start), min(length, end + 1))
        labels[idx] = ((idx - start) % 3 + 1) if strand == 1 else ((end - idx) % 3 + 4)
    return labels


def masked_mean(x, mask):
    """Mean over the sequence dim of x [B, T, d], counting only positions where mask [B, T] is True."""
    m = mask.unsqueeze(-1).to(x.dtype)
    return (x * m).sum(1, keepdim=True) / m.sum(1, keepdim=True)


EMOTION_MODES = ("off", "on", "static", "scalar")


class Emotion(nn.Module):
    """Gain modulation on the residual stream: y = x + alpha * (g * x). Never mixes positions, only rescales.

    mode "on":     g = tanh(W2 GELU(W1 mean_T(x)))  per channel, depends on the input (the layer in the spec)
    mode "static": g = tanh(v)                      per channel, learned constant (control: no input dependence)
    mode "scalar": g = 1                            one gain per block (control: plain residual rescale)
    alpha starts at 0 (ReZero), so every mode starts as identity.
    Deviation from the spec: the mean over T skips padding (a token uses on average ~26 of 64 positions).
    """

    def __init__(self, d_model, mode="on"):
        super().__init__()
        self.mode = mode
        # Forked RNG: the rest of the organ gets the same init with and without this layer.
        with torch.random.fork_rng(devices=[]):
            if mode == "on":
                self.w1 = nn.Linear(d_model, d_model // 4)
                self.w2 = nn.Linear(d_model // 4, d_model)
            elif mode == "static":
                # Non-zero init so alpha gets a gradient at step 0, as in mode "on".
                self.v = nn.Parameter(torch.randn(d_model) * 0.1)
        self.alpha = nn.Parameter(torch.zeros(()))
        self.last_g = None  # [B, d], kept for diagnostics (mode "on" only)

    def forward(self, x, mask):
        if self.mode == "scalar":
            return x + self.alpha * x
        if self.mode == "static":
            return x + self.alpha * (torch.tanh(self.v) * x)
        g = torch.tanh(self.w2(F.gelu(self.w1(masked_mean(x, mask)))))  # [B, 1, d]
        self.last_g = g.squeeze(1).detach()
        return x + self.alpha * (g * x)


class Block(nn.Module):
    """x = x + attn(ln1(x)); [x = emotion(x)]; x = x + ffn(ln2(x))."""

    def __init__(self, d_model, n_heads, ff_mult, dropout, emotion="off"):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_heads, dropout=dropout, batch_first=True)
        self.emotion = Emotion(d_model, emotion) if emotion != "off" else None
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(nn.Linear(d_model, ff_mult * d_model), nn.GELU(),
                                 nn.Linear(ff_mult * d_model, d_model), nn.Dropout(dropout))

    def forward(self, x, mask):
        h = self.ln1(x)
        kpm = None if mask is None else ~mask  # mask None = every position is real (lets SDPA use its fast path)
        x = x + self.attn(h, h, h, key_padding_mask=kpm, need_weights=False)[0]
        if self.emotion is not None:
            x = self.emotion(x, mask)
        return x + self.ffn(self.ln2(x))


class Organ(nn.Module):
    """2-bit symbol sequence -> one vector in the LLM's embedding space.

    Embedding(4, d) + learned positions -> n_layers x Block -> masked mean pool -> Linear(out_dim).
    norm_head=True adds Linear(d, 1) on the pooled state predicting log ||target||, so the output
    magnitude is learned too (the cosine loss only trains the direction).
    impl="torch" is the original nn.TransformerEncoder version, kept so early checkpoints still load.
    """

    def __init__(self, out_dim=768, d_model=64, n_layers=2, n_heads=4, ff_mult=4, dropout=0.0,
                 max_len=MAX_SYMBOLS, emotion="off", impl="custom", norm_head=False):
        super().__init__()
        emotion = {True: "on", False: "off"}.get(emotion, emotion)  # older checkpoints stored a bool
        assert emotion in EMOTION_MODES, emotion
        self.config = dict(out_dim=out_dim, d_model=d_model, n_layers=n_layers, n_heads=n_heads, ff_mult=ff_mult,
                           dropout=dropout, max_len=max_len, emotion=emotion, impl=impl, norm_head=norm_head)
        self.sym_emb = nn.Embedding(N_SYMBOLS, d_model)
        self.pos_emb = nn.Embedding(max_len, d_model)
        if impl == "torch":
            assert emotion == "off", "the emotion layer needs impl='custom'"
            layer = nn.TransformerEncoderLayer(d_model, n_heads, ff_mult * d_model, dropout,
                                               activation="gelu", batch_first=True, norm_first=True)
            self.encoder = nn.TransformerEncoder(layer, n_layers, enable_nested_tensor=False)
        else:
            self.blocks = nn.ModuleList(Block(d_model, n_heads, ff_mult, dropout, emotion) for _ in range(n_layers))
        self.norm = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, out_dim)
        self.norm_head = None
        if norm_head:
            with torch.random.fork_rng(devices=[]):
                self.norm_head = nn.Linear(d_model, 1)

    def emotion_layers(self):
        return [b.emotion for b in getattr(self, "blocks", []) if b.emotion is not None]

    def forward(self, symbols, lengths, return_log_norm=False):
        # symbols: long [B, L], lengths: long [B] (number of real symbols, >= 1)
        L = symbols.shape[1]
        pos = torch.arange(L, device=symbols.device)
        mask = pos[None, :] < lengths[:, None]  # True = real symbol
        x = self.sym_emb(symbols) + self.pos_emb(pos)[None]
        if self.config["impl"] == "torch":
            x = self.encoder(x, src_key_padding_mask=~mask)
        else:
            for block in self.blocks:
                x = block(x, mask)
        pooled = masked_mean(self.norm(x), mask).squeeze(1)
        out = self.head(pooled)
        if return_log_norm:
            return out, self.norm_head(pooled).squeeze(-1) if self.norm_head is not None else None
        return out


class Segmenter(nn.Module):
    """Raw 2-bit stream window -> logits per symbol.

    n_out=1: one boundary logit per symbol ("does a unit end here?"), output [B, W].
    n_out>1: class logits per symbol (e.g. gene structure), output [B, W, n_out].
    Embedding(4, d) -> [conv stem] + learned positions -> n_layers x Block (bidirectional) -> Linear(n_out).
    conv_layers > 0 adds a stem of residual dilated convolutions (kernel 9, dilation 1, 2, 4, ... cycling
    up to 32): local patterns such as the 3-base codon rhythm come for free instead of having to be
    discovered by attention, which got stuck on long loss plateaus without it.
    It sees no byte alignment, no tokens and no characters: only symbols.
    """

    def __init__(self, d_model=256, n_layers=4, n_heads=8, ff_mult=4, dropout=0.0, window=1024, n_out=1,
                 conv_layers=0):
        super().__init__()
        self.config = dict(d_model=d_model, n_layers=n_layers, n_heads=n_heads, ff_mult=ff_mult,
                           dropout=dropout, window=window, n_out=n_out, conv_layers=conv_layers)
        self.sym_emb = nn.Embedding(N_SYMBOLS, d_model)
        dilations = [2 ** (i % 6) for i in range(conv_layers)]
        self.convs = nn.ModuleList(nn.Conv1d(d_model, d_model, 9, padding=4 * d, dilation=d) for d in dilations)
        self.pos_emb = nn.Embedding(window, d_model)
        self.blocks = nn.ModuleList(Block(d_model, n_heads, ff_mult, dropout) for _ in range(n_layers))
        self.norm = nn.LayerNorm(d_model)
        self.out = nn.Linear(d_model, n_out)

    def forward(self, symbols):
        # symbols: long [B, W] with W <= window
        pos = torch.arange(symbols.shape[1], device=symbols.device)
        x = self.sym_emb(symbols)
        if len(self.convs):
            h = x.transpose(1, 2)
            for conv in self.convs:
                h = h + F.gelu(conv(h))
            x = h.transpose(1, 2)
        x = x + self.pos_emb(pos)[None]
        for block in self.blocks:
            x = block(x, None)
        out = self.out(self.norm(x))
        return out.squeeze(-1) if self.config["n_out"] == 1 else out


@torch.no_grad()
def tag_stream(model, symbols: torch.Tensor, batch=32) -> torch.Tensor:
    """Logits [S, n_out] for every symbol of a long 1-D stream (same windowing as segment_stream)."""
    model.eval()
    W, n_out = model.config["window"], model.config["n_out"]
    S = len(symbols)
    out = torch.empty(S, n_out, device=symbols.device)
    starts = [0] if S <= W else list(range(0, S - W + 1, W // 2))
    if S > W and starts[-1] != S - W:
        starts.append(S - W)
    for i in range(0, len(starts), batch):
        st = starts[i : i + batch]
        x = torch.stack([symbols[s : s + min(W, S)] for s in st]).long()
        with torch.autocast(device_type=x.device.type, dtype=torch.bfloat16, enabled=x.is_cuda):
            logits = model(x).float().reshape(len(st), x.shape[1], n_out)
        for j, s in enumerate(st):
            lo = 0 if s == 0 else W // 4
            hi = x.shape[1] if s + x.shape[1] == S else 3 * W // 4
            out[s + lo : s + hi] = logits[j, lo:hi]
    return out


@torch.no_grad()
def segment_stream(model, symbols: torch.Tensor, batch=32) -> torch.Tensor:
    """Boundary probability for every symbol of a long 1-D stream.

    Windows of W with stride W/2; each position is taken from the window where it sits in the middle half
    (the first window also covers its first quarter, the last window its last quarter), so every prediction
    has context on both sides except at the very ends of the stream.
    """
    model.eval()
    W = model.config["window"]
    S = len(symbols)
    if S <= W:
        return torch.sigmoid(model(symbols[None].long())[0].float())
    stride = W // 2
    starts = list(range(0, S - W + 1, stride))
    if starts[-1] != S - W:
        starts.append(S - W)
    probs = torch.empty(S, device=symbols.device)
    for i in range(0, len(starts), batch):
        st = starts[i : i + batch]
        x = torch.stack([symbols[s : s + W] for s in st]).long()
        with torch.autocast(device_type=x.device.type, dtype=torch.bfloat16, enabled=x.is_cuda):
            p = torch.sigmoid(model(x).float())
        for j, s in enumerate(st):
            lo = 0 if s == 0 else W // 4
            hi = W if s == S - W else 3 * W // 4
            probs[s + lo : s + hi] = p[j, lo:hi]
    return probs


def save_model(path: Path, model: nn.Module, extra: dict):
    torch.save({"config": model.config, "state_dict": model.state_dict(), **extra}, path)


def load_segmenter(path: Path, device):
    ckpt = torch.load(path, map_location=device, weights_only=False)
    model = Segmenter(**ckpt["config"]).to(device)  # older checkpoints have no n_out -> 1
    model.load_state_dict(ckpt["state_dict"])
    return model, ckpt


def load_vocab(data_dir: Path, device):
    """Symbol table and lengths for every token id, as tensors on device."""
    symbols = torch.from_numpy(np.load(data_dir / "vocab_symbols.npy").astype(np.int64)).to(device)
    lengths = torch.from_numpy(np.load(data_dir / "vocab_lengths.npy").astype(np.int64)).to(device)
    return symbols, lengths


def load_gpt2_wte(model_name="gpt2"):
    from transformers import GPT2LMHeadModel

    model = GPT2LMHeadModel.from_pretrained(model_name)
    return model.transformer.wte.weight.detach().clone()


def save_organ(path: Path, organ: Organ, extra: dict):
    torch.save({"config": organ.config, "state_dict": organ.state_dict(), **extra}, path)


def load_organ(path: Path, device):
    ckpt = torch.load(path, map_location=device, weights_only=False)
    config = {"impl": "torch"} | ckpt["config"]  # checkpoints from before impl existed are "torch"
    organ = Organ(**config).to(device)
    organ.load_state_dict(ckpt["state_dict"])
    return organ, ckpt


def run_dir(runs_dir: Path) -> Path:
    d = runs_dir / datetime.date.today().isoformat()
    d.mkdir(parents=True, exist_ok=True)
    return d


def update_metrics(out_dir: Path, key: str, value) -> Path:
    """Merge value under key into out_dir/metrics.json (out_dir = a runs/<date> folder).

    Several processes write here at once (training chains, data prep), so the read-modify-write is
    done under a lock file and the new file is swapped in atomically.
    """
    path = out_dir / "metrics.json"
    lock = out_dir / "metrics.json.lock"
    for _ in range(600):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL)
            break
        except FileExistsError:
            if time.time() - lock.stat().st_mtime > 60:  # stale lock from a crashed process
                lock.unlink(missing_ok=True)
            time.sleep(0.1)
    else:
        raise TimeoutError(f"could not lock {path}")
    try:
        metrics = json.loads(path.read_text()) if path.exists() else {}
        metrics[key] = value
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(metrics, indent=2))
        os.replace(tmp, path)
    finally:
        os.close(fd)
        lock.unlink(missing_ok=True)
    return path


class Progress:
    """Live progress of one run for watch.py: runs/progress/<run>.json, rewritten at most every `every` s.

    progress = Progress(runs_dir, "g_aug", total=6000, kind="train_genome")
    progress.update(step, loss=0.12, frame_acc=0.97)   # call every step, it throttles itself
    progress.done(final_metric=0.98)
    """

    def __init__(self, runs_dir: Path, run: str, total: int, kind: str, every: float = 2.0):
        self.path = Path(runs_dir) / "progress" / f"{run}.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.state = {"run": run, "kind": kind, "total": total, "step": 0, "status": "running",
                      "pid": os.getpid(), "started": time.time(), "updated": time.time(), "metrics": {}}
        self.every, self._last = every, 0.0
        self._write()

    def update(self, step: int, force: bool = False, **metrics):
        self.state["metrics"].update({k: float(v) for k, v in metrics.items()})
        self.state["step"] = step
        now = time.time()
        if force or now - self._last >= self.every:
            self._last = now
            self.state["updated"] = now
            self._write()

    def done(self, **metrics):
        self.state["status"] = "done"
        self.update(self.state["total"], force=True, **metrics)

    def _write(self):
        # Never let progress reporting kill a run: on Windows os.replace fails while a reader (watch.py)
        # has the file open. Skip this write; the next update tries again.
        try:
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.state))
            os.replace(tmp, self.path)
        except OSError:
            self._last = 0.0


# ---------- synthetic DNA: gene grammar without any species' accent ----------

import itertools as _it

DNA = "GATC"  # symbol order of the project mapping
STOP_CODONS = ("TAA", "TAG", "TGA")
SENSE_CODONS = tuple(c for c in ("".join(t) for t in _it.product("ACGT", repeat=3)) if c not in STOP_CODONS)
_COMP = str.maketrans("ACGT", "TGCA")
_BASE_LUT = np.zeros(256, dtype=np.uint8)
for _i, _b in enumerate(DNA):
    _BASE_LUT[ord(_b)] = _i


def dna_to_symbols(seq: str) -> np.ndarray:
    return _BASE_LUT[np.frombuffer(seq.encode("ascii"), dtype=np.uint8)]


def codon_usage(symbols: np.ndarray, genes, mask=None) -> np.ndarray:
    """Frequencies of the 61 sense codons inside genes (start and stop codons excluded); mask limits the genes used."""
    seq = "".join(np.array(list(DNA))[symbols])
    counts = dict.fromkeys(SENSE_CODONS, 0)
    for b, e, strand in genes:
        if mask is not None and not (mask[b] and mask[e]):
            continue
        g = seq[b : e + 1] if strand == 1 else seq[b : e + 1].translate(_COMP)[::-1]
        for i in range(3, len(g) - 3, 3):
            if g[i : i + 3] in counts:
                counts[g[i : i + 3]] += 1
    w = np.array([counts[c] for c in SENSE_CODONS], dtype=float)
    return w / w.sum()


def synthetic_dna(gc: float, n_segments: int, rng: np.random.Generator, decoy_usage: np.ndarray):
    """Synthetic sequence alternating filler with genes and decoys.

    gene    ("mechanics"): ATG + random sense codons drawn at the target GC (no species' codon preference)
            + stop. Labelled as a gene.
    decoy   ("accent"): codons drawn from decoy_usage (a real species' preferences) with an in-frame stop
            every ~18 codons. Not a gene: labelled non-coding.
    filler  random bases at the target GC.
    Genes and decoys land on either strand. Returns (symbols uint8, labels int64, genes, kinds) where
    kinds is a list of (start, end, "filler" | "mechanics" | "accent").
    """
    base_p = np.array([gc / 2, (1 - gc) / 2, (1 - gc) / 2, gc / 2])  # G A T C
    sense_w = np.array([np.prod([gc / 2 if b in "GC" else (1 - gc) / 2 for b in c]) for c in SENSE_CODONS])
    sense_w /= sense_w.sum()
    parts, genes, kinds, pos = [], [], [], 0
    for i in range(n_segments):
        for kind in ("filler", "mechanics" if i % 2 == 0 else "accent"):
            if kind == "filler":
                seg = "".join(rng.choice(list(DNA), int(rng.integers(100, 400)), p=base_p))
            else:
                n = int(rng.integers(100, 500))
                if kind == "mechanics":
                    seg = "ATG" + "".join(rng.choice(SENSE_CODONS, n, p=sense_w)) + rng.choice(STOP_CODONS)
                else:
                    codons = list(rng.choice(SENSE_CODONS, n, p=decoy_usage))
                    for k in np.cumsum(rng.geometric(1 / 18, n)):
                        if k < n:
                            codons[k] = rng.choice(STOP_CODONS)
                    seg = "".join(codons)
                strand = 1 if rng.random() < 0.5 else -1
                if strand == -1:
                    seg = seg.translate(_COMP)[::-1]
                if kind == "mechanics":
                    genes.append((pos, pos + len(seg) - 1, strand))
            parts.append(seg)
            kinds.append((pos, pos + len(seg), kind))
            pos += len(seg)
    symbols = dna_to_symbols("".join(parts))
    return symbols, genes_to_labels(len(symbols), genes), genes, kinds


# ---------- audio: raw audio files as 2-bit streams ----------

AUDIO_ENCODINGS = ("pcm16le", "pcm16be", "pcm8", "mulaw")
CTC_CHARS = " 'abcdefghijklmnopqrstuvwxyz"  # CTC class k+1 = CTC_CHARS[k]; class 0 = blank


def encode_audio(pcm: np.ndarray, encoding: str) -> np.ndarray:
    """int16 samples -> the bytes of that audio stored in `encoding` -> 2-bit symbols (4 per byte).

    pcm16le / pcm16be   16-bit signed PCM, little / big endian (8 symbols per sample)
    pcm8                8-bit unsigned PCM, as in 8-bit WAV (4 symbols per sample)
    mulaw               G.711 mu-law, 8 bits (4 symbols per sample)
    """
    x = pcm.astype(np.int16)
    if encoding == "pcm16le":
        data = x.astype("<i2").view(np.uint8)
    elif encoding == "pcm16be":
        data = x.astype(">i2").view(np.uint8)
    elif encoding == "pcm8":
        data = ((x.astype(np.int32) >> 8) + 128).astype(np.uint8)
    elif encoding == "mulaw":
        v = np.clip(x.astype(np.int32), -32635, 32635)
        sign = (v < 0).astype(np.int32)
        mag = np.abs(v) + 0x84
        exponent = np.floor(np.log2(mag)).astype(np.int32) - 7
        mantissa = (mag >> (exponent + 3)) & 0x0F
        data = (~((sign << 7) | (exponent << 4) | mantissa) & 0xFF).astype(np.uint8)
    else:
        raise ValueError(encoding)
    return bytes_to_symbols_np(np.ascontiguousarray(data))


def text_to_ctc(text: str) -> list[int]:
    return [CTC_CHARS.index(c) + 1 for c in text if c in CTC_CHARS]


def ctc_greedy(ids) -> str:
    out, prev = [], 0
    for i in ids:
        if i != prev and i != 0:
            out.append(CTC_CHARS[i - 1])
        prev = i
    return "".join(out)


def edit_distance(a, b) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class AudioOrgan(nn.Module):
    """Raw 2-bit stream of an audio file -> CTC character logits per frame.

    Embedding(4, 32) -> strided conv stem (total stride 2048 symbols: 16 ms of 16-bit audio, 32 ms of
    8-bit audio) -> learned frame positions -> n_layers x Block -> Linear(1 + len(CTC_CHARS)).
    Nothing tells it where a sample starts, which byte is high or how samples are encoded.
    """

    STEM = ((32, 64, 16, 8), (64, 128, 8, 4), (128, 192, 8, 4), (192, 256, 8, 4), (256, 256, 4, 4))

    def __init__(self, d_model=256, n_layers=6, n_heads=4, ff_mult=4, dropout=0.1, max_frames=4096):
        super().__init__()
        self.config = dict(d_model=d_model, n_layers=n_layers, n_heads=n_heads, ff_mult=ff_mult,
                           dropout=dropout, max_frames=max_frames)
        self.sym_emb = nn.Embedding(N_SYMBOLS, 32)
        layers = []
        for c_in, c_out, k, s in self.STEM:
            layers += [nn.Conv1d(c_in, c_out, k, stride=s, padding=(k - s) // 2), nn.GroupNorm(8, c_out), nn.GELU()]
        layers[-3] = nn.Conv1d(256, d_model, 4, stride=4)
        self.stem = nn.Sequential(*layers)
        self.stride = int(np.prod([s for *_, s in self.STEM]))
        self.local = nn.ModuleList(nn.Conv1d(d_model, d_model, 5, padding=2) for _ in range(2))
        self.pos_emb = nn.Embedding(max_frames, d_model)
        self.blocks = nn.ModuleList(Block(d_model, n_heads, ff_mult, dropout) for _ in range(n_layers))
        self.norm = nn.LayerNorm(d_model)
        self.out = nn.Linear(d_model, 1 + len(CTC_CHARS))

    def frames(self, n_symbols: torch.Tensor) -> torch.Tensor:
        return torch.div(n_symbols, self.stride, rounding_mode="floor").clamp(min=1)

    def features(self, symbols, lengths):
        """Frame features [B, F, d] after the last block (normalised), frames [B], mask [B, F]."""
        h = self.stem(self.sym_emb(symbols).transpose(1, 2))
        for conv in self.local:
            h = h + F.gelu(conv(h))
        x = h.transpose(1, 2)
        n = x.shape[1]
        frames = self.frames(lengths).clamp(max=n)
        mask = torch.arange(n, device=x.device)[None] < frames[:, None]
        x = x + self.pos_emb(torch.arange(n, device=x.device).clamp(max=self.config["max_frames"] - 1))[None]
        for block in self.blocks:
            x = block(x, mask)
        return self.norm(x), frames, mask

    def forward(self, symbols, lengths):
        # symbols: long [B, S] (padded), lengths: long [B] symbols per item -> logits [B, F, C], frames [B]
        x, frames, _ = self.features(symbols, lengths)
        return self.out(x), frames


def load_audio_organ(path: Path, device):
    ckpt = torch.load(path, map_location=device, weights_only=False)
    model = AudioOrgan(**ckpt["config"]).to(device)
    model.load_state_dict(ckpt["state_dict"])
    return model, ckpt
