# Proteins recovered from raw nanopore reads — the practical test (H. volcanii, held-out archaeon)

Question: from raw reads, before assembly, which method gives the real proteins? This is what a user
needs (not per-base frame accuracy). Script: `compare_proteins.py`; full table: `proteins_hvolcanii.md`;
queue: `queue_proteins.sh`.

- Organs: labels -> same-strand runs translated with the organ's own codon positions (frameshifts corrected).
- FragGeneScanRs 1.1.0: three sequencing-error models; its best one is quoted.
- DIAMOND 2.2.8 blastx `--long-reads` (-F 15): `panel` = proteins of the 13 training species (what the
  organ saw: no close reference); `self` = H. volcanii's own proteome (oracle, not a fair method).
- Recovered: a gene fully inside a read matched by one predicted protein with >= 80% coverage and
  identity. Precision counts a predicted protein as right if it matches any gene touching the read
  (genes cut by read ends are not false positives).

## 2026 reads (96.3% identity, 299 reads, 3,811 complete genes)
| method | genes recovered | mean identity x coverage | precision |
|---|---|---|---|
| DIAMOND vs own proteome (oracle) | 0.963 | 0.942 | 0.974 |
| **organ panel_aug + decoder** | **0.883** | **0.884** | **0.906** |
| organ panel_ontmix_sub_ft + decoder | 0.879 | 0.883 | 0.903 |
| organ panel_ontmix_ft + decoder | 0.871 | 0.879 | 0.905 |
| FragGeneScanRs (best model, 454_10) | 0.864 | 0.867 | 0.833 |
| Prodigal (meta) | 0.257 | 0.518 | 0.699 |
| DIAMOND vs training species | 0.259 | 0.299 | 0.948 |

## 2020 reads (82.2% identity, 92 complete genes)
No method recovers a protein at >= 80% identity (the reads themselves are 82% identical). Mean identity x
coverage: oracle 0.285, organ panel_ontmix_ft 0.253, FragGeneScanRs (454_30) 0.241, organ panel_aug
0.141, Prodigal 0.033. The thresholds are not informative at this error rate.

## What this shows
1. **The organ is the best non-oracle method on modern reads, but by a small margin**: +1.9 pt genes
   recovered over FragGeneScan's best model (0.883 vs 0.864) and +5.6 pt precision (0.906 vs 0.850 for
   FGS's most precise model). It needs no reference database and no choice of error model.
2. **Prodigal was the wrong opponent**: on raw reads it truncates proteins at every indel (0.26).
   FragGeneScan, built for error-prone reads, is the real baseline and is close.
3. **Without a close reference, homology search fails**: DIAMOND against the 13 training species
   recovers 0.26 (precise, but most H. volcanii proteins have no relative in the database). With the
   perfect reference it reaches 0.96, 8 pt above the organ.
4. The nanopore fine-tunes do not help at protein level on modern reads (0.871-0.879 vs 0.883): their
   gain is at 18% errors, where nobody recovers proteins anyway.

Caveats: one species, one read set, one seed; the organ-vs-FGS gap (1.9 pt) needs error bars (seeds are
queued) and more held-out species before it is a claim.
