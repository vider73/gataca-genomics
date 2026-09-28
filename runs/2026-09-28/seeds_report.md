# Seeds: error bars for the three organs (2026-09-28)

Three seeds per organ: `panel_aug` trained from scratch (seeds 0, 1, 2) and its two nanopore fine-tunes
initialised from the same seed's panel_aug. Mean ± standard deviation over the 3 seeds.
Queues: `queue_seeds.sh`, `queue_proteins_seeds.sh`; tables `genomics_panel_*_s*.md`, `nanopore_hvolcanii.md`,
`proteins_hvolcanii.md`.

## Proteins recovered from raw 2026 nanopore reads (H. volcanii, held-out; organ + grammar decoder)
| | genes recovered | precision |
|---|---|---|
| **panel_aug** | **0.885 ± 0.003** | **0.903 ± 0.003** |
| panel_ontmix_sub_ft | 0.879 ± 0.001 | 0.899 ± 0.004 |
| panel_ontmix_ft | 0.870 ± 0.002 | 0.900 ± 0.004 |
| FragGeneScanRs, best of 3 error models (deterministic) | 0.864 | 0.833-0.850 |
| DIAMOND blastx -F vs the 13 training species | 0.259 | 0.948 |
| Prodigal (meta) | 0.257 | 0.699 |
| DIAMOND vs H. volcanii's own proteome (oracle) | 0.963 | 0.974 |

All three panel_aug seeds beat FragGeneScan's best model (0.883, 0.888, 0.882 vs 0.864): the gap
(+2.1 pt recall, +5 pt precision) is ~7x the seed standard deviation. This was the publication criterion
fixed before the seeds ran.

## Reading frame on real reads
| | 2026 reads (decoder) | 2020 reads (organ alone) |
|---|---|---|
| panel_aug | 0.947 ± 0.000 | 0.386 ± 0.016 |
| panel_ontmix_ft | 0.945 ± 0.000 | 0.535 ± 0.008 |
| panel_ontmix_sub_ft | 0.947 ± 0.001 | 0.535 ± 0.009 |

## Panel robustness, mean over the 5 held-out species
| | frame clean | genes (decoder) clean | frame 5% subs | frame 1% indels | frame 150 bp fragments |
|---|---|---|---|---|---|
| panel_aug | 0.987 ± 0.000 | 0.927 ± 0.002 | 0.970 ± 0.000 | 0.902 ± 0.000 | 0.942 ± 0.003 |
| panel_ontmix_ft | 0.983 ± 0.001 | 0.934 ± 0.001 | 0.956 ± 0.002 | 0.898 ± 0.001 | 0.931 ± 0.004 |
| panel_ontmix_sub_ft | 0.985 ± 0.001 | 0.921 ± 0.001 | 0.968 ± 0.001 | 0.901 ± 0.001 | 0.936 ± 0.005 |
| Prodigal (single run) | 0.991 | 0.980 (own genes) | 0.861 | 0.499 | 0.913 |

## What this settles
- Seed noise is small (<= 0.5 pt almost everywhere, 1.6 pt on the 2020 reads): the earlier single-seed
  differences were real.
- **panel_aug is the default organ**: best on proteins and modern reads. The nanopore fine-tunes are
  only worth it on very noisy (old-chemistry) reads, where they read 0.535 of the frame instead of 0.386.
- Still one held-out species for real reads; more species (and simulated nanopore reads) remain to do.
