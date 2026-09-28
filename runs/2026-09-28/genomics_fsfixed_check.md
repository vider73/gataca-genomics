# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_ontmix_ft | 0.978 | 0.972 | 0.503 / 0.473 | 0.882 / 0.830 | 0.911 / 0.885 | 0.696 / 0.576 | 0.395 / 0.106 | 0.975 | 0.954 | 0.293 / 0.188 | 0.891 | 0.178 | 0.937 |
| bsubtilis (whole genome, held-out species) | genome_panel_ontmix_ft | 0.977 | 0.985 | 0.386 / 0.311 | 0.879 / 0.708 | 0.926 / 0.866 | 0.637 / 0.442 | 0.392 / 0.110 | 0.971 | 0.931 | 0.210 / 0.112 | 0.853 | 0.119 | 0.893 |
