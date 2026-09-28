# Nanopore error model in training — real reads of H. volcanii (held-out archaeon)

Question: does training with a realistic nanopore error model (instead of uniform subs + indels)
help on real nanopore reads?

Error model (`gataca.mutate_nanopore`, from published nanopore error profiles, not fit to our reads):
total rate per window drawn from [0, err_max]; split sub / ins / del around 35 / 25 / 40% (Dirichlet);
indels 4x more likely inside homopolymers (>= 3 equal bases), where insertions repeat the run's base;
bursty (log-normal local rate, sigma 0.7, changing every ~200 bases).

Organs (same architecture and 12k steps on the same 13 training species as `panel_aug`):
- `panel_ont`: nanopore errors, err_max 15%.
- `panel_ont25`: nanopore errors, err_max 25%.
- `panel_aug` (reference): uniform noise, subs <= 5%, indels <= 2%.

Full table: `nanopore_hvolcanii.md` (this run); log `runs/eval_nanopore_ont.log`.

## Real reads, frame accuracy (organ + grammar decoder)
| | 2026 reads (96.3% identity) | same stretch, no errors | 2020 reads (82.2% identity) |
|---|---|---|---|
| **panel_aug** | **0.947** | **0.989** | 0.367 (organ alone 0.386) |
| panel_ont | 0.939 | 0.980 | 0.498 (organ alone 0.525) |
| panel_ont25 | 0.934 | 0.974 | 0.517 (organ alone **0.544**) |
| Prodigal (meta) | 0.577 | 0.994 | 0.106 |
| ORF rule | 0.345 | 0.692 | 0.038 |

Genes with the exact stop codon, 2026 reads: panel_aug 0.616, panel_ont 0.585, panel_ont25 0.573,
Prodigal 0.500. On the 2020 reads genes stay ~0 for every method (92 genes fully inside reads).

## Validation windows during training (13 training species)
| | frame clean | uniform noise (5% sub, 2% indel) | nanopore model 8% |
|---|---|---|---|
| panel_aug (step 10 of a fine-tune, ~its own value) | 0.985 | 0.888 | 0.699 |
| panel_ont | 0.975 | 0.872 | 0.722 |
| panel_ont25 | 0.970 | 0.863 | 0.720 |
Curves were flat from step ~5k on.

## What this shows
1. **On modern reads (~4% errors) the nanopore model does not help; it costs ~1 pt** (0.939 / 0.934 vs
   0.947), and it costs the same ~1 pt on error-free sequence. panel_aug's uniform noise already
   covers the modern error range; training on up to 15-25% errors spends capacity on a regime these
   reads do not have.
2. **On old reads (18% errors) it helps a lot: frame acc 0.39 -> 0.53-0.54** (Prodigal 0.11). The organ
   now reads more than half of the reading frame through 18% errors in an unseen species. Still no
   exact genes at that error rate.
3. The grammar decoder helps on modern reads (+0.4-0.5 pt) and hurts slightly on the old ones
   (-2.7 pt): its soft grammar assumes errors are rare.
4. Validation on the synthetic nanopore model at 8% moves only from 0.70 to 0.72: with an indel every
   ~20 bases, frame recovery is probably near an information limit for this organ.

## Next
- Match the error-rate distribution to the target instead of uniform [0, max]: most windows at low
  rates (e.g. exponential, mean ~4%) with a tail to 20%. Aim: keep panel_aug on modern reads and
  panel_ont25 on old reads in one organ.
- Or fine-tune panel_aug briefly with the nanopore model (--init) and compare.
- Let the grammar decoder's frameshift cost depend on the expected error rate.

## Update 2026-09-28: skewed error-rate distribution — one organ for both regimes
`panel_ontmix_ft`: panel_aug fine-tuned 4k steps (lr 2e-4) with the nanopore model and `--err-dist mix`:
per window, with p 0.85 the rate is exponential with mean 4% (capped at 25%), otherwise uniform in
[0, 25%] (median 3.3%, 8% of windows above 15%). Log: `runs/eval_nanopore_ontmix_ft.log`.

| frame acc (organ + grammar decoder) | 2026 reads | same stretch, no errors | 2020 reads (organ alone) | genes exact stop, 2026 reads |
|---|---|---|---|---|
| panel_aug | **0.947** | **0.989** | 0.386 | 0.616 |
| panel_ont25 | 0.934 | 0.974 | **0.544** | 0.573 |
| **panel_ontmix_ft** | 0.945 | 0.988 | 0.542 | **0.618** |
| Prodigal | 0.577 | 0.994 | 0.106 | 0.500 |

- **One organ now covers both regimes:** within 0.2 pt of panel_aug on modern reads and on error-free
  sequence, and within 0.2 pt of panel_ont25 on 18%-error reads. The goal (>= 0.947 / >= 0.54) is met
  up to 0.2 pt.
- The error-rate distribution was the problem, not the error model: uniform [0, max] spent most
  windows at high error rates.
- Validation (13 training species): clean 0.983, uniform noise 0.883, nanopore 8% 0.721.
- Note: this fine-tune (and the queued from-scratch `panel_ontmix`) shared the GPU overnight, so its
  wall time (5 h) is not representative (~15 min alone).

### From scratch vs fine-tune, and the panel robustness table (2026-09-28, queue_ontmix2.sh)
`panel_ontmix`: same recipe from scratch, 12k steps (21 min alone on the GPU). Logs:
`runs/eval_nanopore_ontmix.log`, `runs/2026-09-28/genomics_panel_ontmix_ft.md`, `genomics_hvolcanii_ont.md`.

| real reads (organ + decoder; 2020: organ alone) | 2026 reads | genes 2026 | error-free | 2020 reads |
|---|---|---|---|---|
| panel_aug | **0.947** | 0.616 | **0.989** | 0.386 |
| panel_ontmix (scratch) | 0.942 | 0.607 | 0.985 | 0.523 |
| **panel_ontmix_ft** | 0.945 | **0.618** | 0.988 | **0.542** |

Fine-tuning the uniform-noise organ beats training the same recipe from scratch on every column.

Panel robustness, mean over the 5 held-out species (Prodigal / panel_aug / panel_ont / panel_ont25 / panel_ontmix_ft):
| | Prodigal | panel_aug | panel_ont | panel_ont25 | panel_ontmix_ft |
|---|---|---|---|---|---|
| frame acc clean | **0.991** | 0.987 | 0.969 | 0.960 | 0.983 |
| genes, grammar decoder | — (0.980 own) | 0.930 | 0.890 | 0.863 | **0.934** |
| frame acc 5% subs | 0.861 | **0.971** | 0.939 | 0.930 | 0.956 |
| frame acc 1% indels | 0.499 | **0.902** | 0.886 | 0.878 | 0.900 |
| frame acc 150 bp fragments | 0.913 | **0.943** | 0.908 | 0.896 | 0.932 |
| genes decoder, 5% subs | 0.637 | **0.727** | 0.679 | 0.663 | 0.709 |
| genes decoder, 1% indels | — | **0.406** | 0.377 | 0.361 | 0.400 |
The 13 training species (validation blocks) give the same ordering.

- panel_ontmix_ft keeps panel_aug's robustness except under uniform 5% substitutions (-1.5 pt) and
  150 bp fragments (-1.1 pt): the nanopore model has fewer substitutions than the old uniform noise.
  In exchange it reads 18%-error nanopore reads at 0.54 instead of 0.39.
- panel_ont / panel_ont25 (uniform rate up to 15 / 25%) lose 2-4 pt everywhere on clean and uniform
  noise: confirms that the rate distribution, not the error model, was the issue.

### Error-rate-aware frameshift cost in the decoder (2026-09-28)
`eval_genome.frameshift_cost`: per sequence, the frameshift cost is -log of how often the organ's argmax
breaks the codon cycle inside coding runs, clipped to [2, 6] nats (default fixed cost: 6). No tuned knob.
Organ: panel_ontmix_ft. Logs: `runs/eval_nanopore_fsauto.log`, `runs/2026-09-28/genomics_fsauto_adaptive.md`.

| decoder | 2026 reads frame / genes | 2020 reads frame | E. coli genes clean / 5% subs / 1% indels | B. subtilis same |
|---|---|---|---|---|
| fixed cost 6 | 0.945 / **0.618** | 0.516 | 0.911 / **0.696** / **0.395** | **0.926** / **0.637** / **0.392** |
| adaptive | **0.946** / 0.614 | **0.530** | 0.911 / 0.694 / 0.393 | 0.925 / 0.633 / 0.386 |
| (organ alone) | 0.943 / 0.590 | 0.542 | | |

- Only the 18%-error reads gain (+1.4 pt), still below the organ alone: the frameshift cost is not
  what hurts the decoder there. Elsewhere it is neutral to slightly negative (up to -0.6 pt genes).
- Kept as an option (`grammar_decode(..., adaptive=True)`), off by default. The decoder's loss on very
  noisy reads more likely comes from the other fixed costs (internal stops appear with 7% substitutions)
  and from exact-stop placement; not pursued, the gain would be small.
