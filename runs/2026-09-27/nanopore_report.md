# Real nanopore reads — H. volcanii (held-out archaeon, GC 66%)

Reads aligned with minimap2 (map-ont) to the main chromosome. Each read base gets its reference
position, or -1 if the sequencer inserted it. Each read is processed on its own, as before assembly.
Full table: `nanopore_hvolcanii.md`.

| run | chemistry | read identity | errors (sub / ins / del) | reads scored | bases |
|---|---|---|---|---|---|
| ERR17000570 | 2026 | 96.3% | 1.1% / 1.2% / 1.5% | 299 (random subset) | 4.0 M |
| SRR11991309 | 2020 | 82.2% | 7.4% / 4.5% / 5.9% | 1,608 (all kept) | 0.69 M |

## Modern reads (96.3% identity)
| | frame acc, real reads | frame acc, same stretch without errors | genes found (exact stop), real reads |
|---|---|---|---|
| **organ panel_aug + grammar decoder** | **0.947** | 0.989 | **0.616** |
| organ panel_syn + grammar decoder | 0.943 | 0.987 | 0.609 |
| Prodigal (meta mode) | 0.577 | **0.994** | 0.500 |
| ORF rule | 0.345 | 0.692 | 0.175 |

- On real sequencing errors, in a species it never saw, the organ keeps **94.7%** of the reading
  frame; Prodigal keeps **57.7%**. Without errors both are ~0.99, so the gap is the errors.
- Genes with the exact stop codon: 0.62 vs 0.50. Every method's precision is low here (0.22–0.33)
  because genes cut by a read's end count as false predictions (only genes fully inside a read are
  in the truth set). That penalises all methods alike, but it needs a fairer definition before
  quoting precision.
- The grammar decoder adds a little at gene level (+1.6 pt) and nothing per base.

## Old reads (82% identity)
Everything collapses: organ 0.39 frame acc, Prodigal 0.11, ORF 0.04; genes ~0 for all. 18% errors
are far beyond the organ's training noise (<= 5% subs, <= 2% indels). The organ degrades least.

## Takeaways
- The main claim holds on **real** data: with modern nanopore reads, the organ reads coding frames
  far better than the standard tool, on a held-out species and domain (archaea).
- Next: train with a realistic error model (nanopore error profile, 2–10%), a fair precision for
  reads, and the comparison tools built for error-prone reads (FragGeneScan).
