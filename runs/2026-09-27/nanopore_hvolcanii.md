# Real nanopore reads — hvolcanii (held-out species)

reads = the real reads; clean = the same reference stretches without sequencing errors.
Each read is processed on its own. Prodigal runs in metagenomic mode.

| run | read identity | input | target | frame acc | coding F1 | genes sens / prec (exact stop) | genes in reads |
|---|---|---|---|---|---|---|---|
| ERR17000570 | 96.3% | reads | genome_panel_aug | 0.945 | 0.974 | 0.600 / 0.219 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_aug + grammar decoder | 0.947 | 0.975 | 0.616 / 0.222 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ont | 0.935 | 0.970 | 0.560 / 0.209 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ont + grammar decoder | 0.939 | 0.971 | 0.585 / 0.214 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ont25 | 0.929 | 0.966 | 0.539 / 0.201 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ont25 + grammar decoder | 0.934 | 0.968 | 0.573 / 0.210 | 3811 |
| ERR17000570 | 96.3% | reads | orf | 0.345 | 0.834 | 0.175 / 0.178 | 3811 |
| ERR17000570 | 96.3% | reads | prodigal | 0.577 | 0.865 | 0.500 / 0.330 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug | 0.988 | 0.980 | 0.937 / 0.806 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug + grammar decoder | 0.989 | 0.981 | 0.945 / 0.837 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ont | 0.977 | 0.975 | 0.886 / 0.717 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ont + grammar decoder | 0.980 | 0.977 | 0.907 / 0.793 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ont25 | 0.970 | 0.971 | 0.856 / 0.674 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ont25 + grammar decoder | 0.974 | 0.973 | 0.882 / 0.765 | 3811 |
| ERR17000570 | 96.3% | clean | orf | 0.692 | 0.906 | 0.632 / 0.722 | 3811 |
| ERR17000570 | 96.3% | clean | prodigal | 0.994 | 0.984 | 0.986 / 0.857 | 3811 |
| SRR11991309 | 82.2% | reads | genome_panel_aug | 0.386 | 0.715 | 0.022 / 0.003 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_aug + grammar decoder | 0.367 | 0.703 | 0.022 / 0.002 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ont | 0.525 | 0.798 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ont + grammar decoder | 0.498 | 0.795 | 0.022 / 0.003 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ont25 | 0.544 | 0.797 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ont25 + grammar decoder | 0.517 | 0.800 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | orf | 0.038 | 0.370 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | prodigal | 0.106 | 0.498 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug | 0.989 | 0.985 | 0.924 / 0.100 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug + grammar decoder | 0.990 | 0.987 | 0.957 / 0.103 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ont | 0.975 | 0.839 | 0.870 / 0.093 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ont + grammar decoder | 0.980 | 0.850 | 0.935 / 0.068 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ont25 | 0.971 | 0.842 | 0.848 / 0.085 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ont25 + grammar decoder | 0.977 | 0.881 | 0.946 / 0.102 | 92 |
| SRR11991309 | 82.2% | clean | orf | 0.280 | 0.502 | 0.598 / 0.206 | 92 |
| SRR11991309 | 82.2% | clean | prodigal | 0.991 | 0.777 | 0.989 / 0.054 | 92 |
