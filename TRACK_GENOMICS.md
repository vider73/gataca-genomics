# GATACA — Genomics track

Organs that read raw DNA (natively 2-bit: G/A/T/C = 00/01/10/11, the project's mapping) and find
gene structure themselves, robustly: sequencing errors, fragments, unseen species. Codons (3 bases)
play the role of bytes; the reading frame plays the role of byte alignment. Shared idea, rules and
infrastructure: `GATACA.md`. The tokenizer track (text, audio, image) lives in `TRACK_TOKENIZERS.md`.

**Location (since 2026-09-28):** `I:\LLMLab\GaTaCa-Genomics`, private repo `github.com/vider73/gataca-genomics`.
The tokenizer track stays in `I:\LLMLab\GaTaCa` (repo `vider73/gataca-tokenizers`). Both share the 4090:
one job at a time through the lab-wide queue `python I:/LLMLab/GPUControl/gpu.py run --project genomics
--name <job> -- <cmd>` (`gpu_idle.py` now defers to `gpu.py status`); long jobs run detached with
`detach.ps1` whose command is a queue script (e.g. `runs/2026-09-28/queue_ontsub_gpu.sh`).

## Status (2026-09-27)
G1 (gene structure in bacteria) is done up to real nanopore reads. Main result: on real 2026 nanopore
reads of a held-out archaeon, the organ keeps **94.7%** of the reading frame vs **57.7%** for Prodigal.

## Data (all in `data/`)
- `genome_<name>/`: per genome `symbols.npy`, `labels.npy` (7 classes: non-coding; forward codon
  position 1-3; reverse codon position 1-3), `split.npy` (100 kb blocks 8/1/1), `genes.npy`, `meta.json`.
- `panel.json`: 18 species resolved from NCBI RefSeq (`prepare_genome.py --panel`), GC 29-72%,
  two archaea. 13 "train" (their train blocks are used), 5 held-out "test": bsubtilis, spneumoniae,
  dradiodurans, tthermophilus, hvolcanii (archaeon).
- `nanopore/<run>/`: real reads aligned with minimap2 (run inside WSL, binary in
  `tools/minimap2-2.31_x64-linux/`), reference-oriented, each read base with its reference position
  (-1 = inserted by the sequencer). Runs: SRR11991309 (2020, 82.2% identity), ERR17000570 (2026, 96.3%).

## Scripts
| step | script |
|---|---|
| genomes + labels (single or `--panel`) | `prepare_genome.py` |
| train organ (`--panel`, `--noise aug\|ont`, `--err-max`, `--init`, `--synthetic-frac`, `--conv-layers`) | `train_genome.py` |
| robustness table vs ORF rule and Prodigal (`--panel`); baselines cached | `eval_genome.py` |
| grammar vs accent probe (synthetic genes / decoys) | `probe_synthetic.py` |
| real nanopore reads: align, then evaluate | `prepare_nanopore.py`, `eval_nanopore.py` |
| proteins recovered from raw reads vs Prodigal, FragGeneScanRs, DIAMOND blastx -F (`tools/`) | `compare_proteins.py` |
Model: `gataca.Segmenter(n_out=7, conv_layers=6)` (~7M params). Grammar decoder: Viterbi with a soft
gene grammar in `eval_genome.grammar_decode` (then codon-cycle split + stop snap).
Nanopore error model for training: `gataca.mutate_nanopore` (indel-heavy, homopolymer-biased, bursty; from
published profiles, not fit to our reads).
Checkpoints: `runs/2026-09-26/genome_panel_aug.pt` (best on modern reads), `genome_panel_syn.pt`;
`runs/2026-09-27/genome_panel_ont.pt` / `genome_panel_ont25.pt` (nanopore errors up to 15% / 25%),
`runs/2026-09-27/genome_panel_ontmix_ft.pt` (**recommended for reads**: good on modern and old reads).
`runs/2026-09-28/genome_panel_ontmix_sub_ft.pt` (same + extra substitutions; best 5%-subs robustness of the two).
GPU: one local job at a time; queue scripts wait on `gpu_idle.py` (e.g. `runs/2026-09-28/queue_ontmix2.sh`).

## Results so far
- A plain transformer stalls at chance (frame acc ~0.30); a dilated conv stem fixes it (0.95 in 600 steps).
- Trained on E. coli only it learns the species' "accent" and collapses on high-GC T. thermophilus (0.185).
- **Panel of 13 species** (`genomics_panel_report.md`), mean over the 5 held-out species:
  frame acc 0.987 (Prodigal 0.991); 5% subs 0.971 vs 0.861; **1% indels 0.902 vs 0.499**;
  150 bp fragments 0.943 vs 0.913.
- **Gene level** (exact stop codon), held-out mean: organ alone 0.55; + stop snap 0.922;
  **+ grammar decoder 0.930** (Prodigal 0.980). With 5% substitutions: **decoder 0.727 vs Prodigal 0.637**.
  With 1% indels: decoder 0.406 (Prodigal's gene-level number under indels not computed yet).
- **Grammar vs accent** (`synthetic_probe.md`): trained on real genomes only, organs ignore gene grammar
  (grammar-only genes called coding 1-34%) and noise training teaches them to distrust stop codons.
  Mixing 25% synthetic DNA (`panel_syn`) flips the probe (86-96% vs decoys 0.3-2.3%) at a small cost
  on real genomes. Caveat: the probe uses the same generator as the synthetic training data.
- **Real nanopore reads** (`nanopore_report.md`), H. volcanii: 2026 chemistry (96.3% identity):
  frame acc organ 0.947 vs Prodigal 0.577; genes (exact stop) 0.62 vs 0.50. 2020 chemistry (82%):
  everything collapses (organ 0.39, Prodigal 0.11).
- **Nanopore error model in training** (`nanopore_ont_report.md`): on 2026 reads it does not help
  (0.939 / 0.934 vs panel_aug 0.947) and costs ~1 pt on clean sequence; on 2020 reads (18% errors) it
  lifts frame acc **0.39 -> 0.54** (panel_ont25; Prodigal 0.11). Exact genes stay ~0 at 18% errors.
- **One organ for both** (`panel_ontmix_ft`: panel_aug + 4k-step nanopore fine-tune, error rate skewed low,
  `--err-dist mix`): 2026 reads 0.945 (genes 0.618), error-free 0.988, 2020 reads 0.542. Matches the best
  specialist in each regime within 0.2 pt. The error-rate distribution mattered, not the error model.
  Fine-tune beats the same recipe from scratch (0.942 / 0.523). Panel robustness (held-out mean) stays
  at panel_aug's level (genes via decoder 0.934 vs 0.930; 1% indels 0.900 vs 0.902) except 5% uniform
  substitutions (0.956 vs 0.971) and 150 bp fragments (0.932 vs 0.943).

## Next (in priority order)
1. Seeds (3 per organ) for panel_aug, panel_ontmix_ft and panel_ontmix_sub_ft (4k-step fine-tunes are
   ~7 min each): the three differ by <= 1.5 pt, so pick the default organ with error bars.
   (Done: extra substitutions in the nanopore mix, `--ont-sub-max 0.05` -> panel_ontmix_sub_ft recovers
   5%-subs robustness 0.969 vs 0.971 and keeps the nanopore gains, but loses 1.2 pt clean gene recall.)
   (Tried: error-rate-aware frameshift cost in the decoder: +1.4 pt on 18%-error reads only, slightly
   negative elsewhere; kept as an option, off by default. See `nanopore_ont_report.md`.)
2. Fair precision on reads (genes cut by read ends), and Prodigal's gene-level numbers under indels.
3. Compare with tools built for error-prone reads (FragGeneScan) and a neural gene finder (Balrog).
4. A grammar probe independent of the synthetic generator (e.g. real proteins back-translated with a
   foreign codon table).
5. Seeds and more held-out species for error bars.
6. G2: a published genomic benchmark (Genomic Benchmarks / Nucleotide Transformer tasks).
7. Later: learned units on DNA (the tokenizer idea applied to genomes); eukaryotes with introns.

## Publication view
Most promising claim: frameshift-robust gene reading on unseen species, validated on real nanopore
reads. Needs 1-5 above before a bioRxiv preprint or an ML-for-biology workshop.
