# Genomics G1 — panel of 18 species, grammar vs accent (2026-09-27)

Organs: 7M params (6-layer dilated conv stem + 4 attention blocks), per-base 7-class gene structure.
- `g_conv_aug`: E. coli only, noise-augmented (5% subs, 2% indels max).
- `panel_aug`: 13 training species (GC 29–72%, incl. an archaeon), noise-augmented, 12k steps.
- `panel_syn`: same plus 25% synthetic DNA per batch (grammar-only genes + accent-only decoys).
Held-out species (never trained on): B. subtilis, S. pneumoniae, D. radiodurans, T. thermophilus,
H. volcanii (archaeon). Full tables: `genomics_panel.md`, `synthetic_probe.md`.

## Mean over the 5 held-out species
| | frame acc clean | genes (exact stop) | genes + stop snap | frame acc 5% subs | frame acc 1% indels | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|
| Prodigal (self-trains on each genome) | **0.991** | **0.980** | — | 0.861 | 0.499 | 0.913 |
| ORF rule | 0.824 | 0.735 | — | 0.519 | 0.225 | 0.422 |
| E. coli-only organ | 0.774 | 0.108 | 0.587 | 0.733 | 0.664 | 0.719 |
| **panel_aug** | 0.987 | 0.551 | **0.922** | **0.971** | **0.902** | **0.943** |
| panel_syn | 0.983 | 0.394 | 0.903 | 0.962 | 0.892 | 0.924 |

The 13 training species (validation blocks) give the same picture: panel_aug 0.989 / 0.929 (snap)
/ 0.976 / 0.908 / 0.956, vs Prodigal 0.994 / 0.985 / 0.841 / 0.516 / 0.914.

## Synthetic probe (grammar-only genes vs accent-only decoys, 3 GC levels)
| | grammar genes called coding ↑ | accent decoys called coding ↓ |
|---|---|---|
| ORF rule | 0.99–1.00 | 0.12–0.16 |
| Prodigal | 0.95–1.00 | 0.26–0.39 |
| E. coli-only organ | 0.10–0.34 | 0.69–0.79 |
| panel_aug | 0.01–0.34 | 0.54–0.65 |
| **panel_syn** | **0.86–0.96** | **0.003–0.023** |

## What this shows
1. **Many species removes the accent problem on real genomes.** Trained on E. coli alone, the organ
   collapses on high-GC T. thermophilus (frame acc 0.185). Trained on the panel, it reads the
   unseen species at 0.98–0.99, within ~0.5 pt of Prodigal, which retrains itself on each genome.
2. **It is far more robust to sequencing errors than Prodigal, on species it never saw:** frame acc
   0.902 vs 0.499 with 1% indels, 0.971 vs 0.861 with 5% substitutions, and 0.943 vs 0.913 on 150 bp
   fragments. This is the advantage we were looking for, and it holds across all 18 species.
3. **One grammar rule fixes most of the gene-level gap:** snapping each gene end to the nearest
   in-frame stop codon lifts exact-stop gene recall from 0.55 to 0.92 (Prodigal: 0.98). The organ
   knows the frame. The explicit rule places the boundary.
4. **Grammar is learnable, but it was not learned from real genomes alone.** panel_aug, with 13
   species, still ignores the grammar (grammar-only genes called coding 1–34%) and still relies on
   composition (decoys 54–65%). Noise augmentation teaches it to distrust stop codons, because
   mutations create fake ones. Adding synthetic grammar examples (panel_syn) flips the probe
   completely (86–96% vs 0.3–2.3%), at a small cost on real genomes (0.3–2 pt).
5. **Caveat on 4:** the probe uses the same generator as the synthetic training data (different
   seed), so part of panel_syn's probe score can be "recognising the generator". A probe built
   differently (e.g. real protein sequences back-translated with a foreign codon table, or genes
   with real stops removed) is needed before calling it grammar.
6. The organs still place exact gene ends poorly on their own (0.39–0.55). A decoder that enforces
   gene grammar (start ... in-frame codons ... stop, e.g. Viterbi over the organ's per-base
   probabilities) is the natural next step, instead of the post-hoc snap.

## Next
- Grammar-constrained decoding (Viterbi / HMM on the organ's probabilities) at gene level, under noise.
- A probe that is independent of the synthetic generator (see 5).
- Real sequencing errors: public nanopore reads of a held-out species, raw vs polished.
