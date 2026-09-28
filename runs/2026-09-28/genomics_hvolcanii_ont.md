# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hvolcanii (whole genome, held-out species) | genome_panel_ont | 0.972 | 0.972 | 0.457 / 0.393 | 0.876 / 0.753 | 0.907 / 0.854 | 0.722 / 0.647 | 0.392 / 0.113 | 0.967 | 0.947 | 0.321 / 0.255 | 0.905 | 0.170 | 0.915 |
| hvolcanii (whole genome, held-out species) | genome_panel_ont25 | 0.964 | 0.968 | 0.289 / 0.243 | 0.849 / 0.713 | 0.877 / 0.819 | 0.706 / 0.628 | 0.378 / 0.110 | 0.960 | 0.940 | 0.204 / 0.153 | 0.899 | 0.108 | 0.910 |
| hvolcanii (whole genome, held-out species) | prodigal | 0.991 | 0.984 | 0.987 / 0.962 | — | — | — | — | 0.956 | 0.852 | 0.662 / 0.416 | 0.374 | — | 0.927 |
| hvolcanii (whole genome, held-out species) | orf | 0.743 | 0.927 | 0.640 / 0.773 | — | — | — | — | 0.685 | 0.471 | 0.277 / 0.291 | 0.256 | — | 0.221 |
