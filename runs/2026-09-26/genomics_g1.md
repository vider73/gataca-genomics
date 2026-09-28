# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | orf | 0.918 | 0.950 | 0.798 / 0.944 | 0.841 | 0.598 | 0.317 / 0.311 | 0.219 | — | 0.593 |
| ecoli (validation blocks) | prodigal | 0.991 | 0.978 | 0.953 / 0.945 | 0.966 | 0.846 | 0.592 / 0.329 | 0.528 | — | 0.902 |
| ecoli (validation blocks) | genome_g_conv_none | 0.978 | 0.973 | 0.634 / 0.632 | 0.968 | 0.910 | 0.382 / 0.237 | 0.391 | 0.094 | 0.892 |
| ecoli (validation blocks) | genome_g_conv_aug | 0.975 | 0.970 | 0.312 / 0.288 | 0.973 | 0.957 | 0.228 / 0.178 | 0.891 | 0.120 | 0.930 |
| bsubtilis (whole genome, held-out species) | orf | 0.926 | 0.958 | 0.821 / 0.975 | 0.844 | 0.576 | 0.301 / 0.320 | 0.209 | — | 0.654 |
| bsubtilis (whole genome, held-out species) | prodigal | 0.993 | 0.992 | 0.975 / 0.977 | 0.956 | 0.825 | 0.545 / 0.313 | 0.502 | — | 0.874 |
| bsubtilis (whole genome, held-out species) | genome_g_conv_none | 0.948 | 0.970 | 0.424 / 0.350 | 0.919 | 0.765 | 0.190 / 0.126 | 0.273 | 0.039 | 0.688 |
| bsubtilis (whole genome, held-out species) | genome_g_conv_aug | 0.950 | 0.973 | 0.127 / 0.084 | 0.943 | 0.897 | 0.076 / 0.041 | 0.804 | 0.046 | 0.825 |
