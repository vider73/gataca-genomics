# Real nanopore reads — hvolcanii (held-out species)

reads = the real reads; clean = the same reference stretches without sequencing errors.
Each read is processed on its own. Prodigal runs in metagenomic mode.

| run | read identity | input | target | frame acc | coding F1 | genes sens / prec (exact stop) | genes in reads |
|---|---|---|---|---|---|---|---|
| ERR17000570 | 96.3% | reads | genome_panel_aug | 0.945 | 0.974 | 0.600 / 0.219 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_aug + grammar decoder | 0.947 | 0.975 | 0.616 / 0.222 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft | 0.943 | 0.974 | 0.590 / 0.220 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft + grammar decoder | 0.945 | 0.974 | 0.618 / 0.225 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_sub_ft | 0.945 | 0.974 | 0.595 / 0.221 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_sub_ft + grammar decoder | 0.946 | 0.974 | 0.613 / 0.223 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug | 0.988 | 0.980 | 0.937 / 0.806 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug + grammar decoder | 0.989 | 0.981 | 0.945 / 0.837 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft | 0.986 | 0.980 | 0.934 / 0.793 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft + grammar decoder | 0.988 | 0.981 | 0.949 / 0.841 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_sub_ft | 0.988 | 0.980 | 0.933 / 0.805 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_sub_ft + grammar decoder | 0.989 | 0.981 | 0.938 / 0.834 | 3811 |
| SRR11991309 | 82.2% | reads | genome_panel_aug | 0.386 | 0.715 | 0.022 / 0.003 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_aug + grammar decoder | 0.367 | 0.703 | 0.022 / 0.002 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft | 0.542 | 0.793 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft + grammar decoder | 0.516 | 0.793 | 0.043 / 0.004 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_sub_ft | 0.536 | 0.812 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_sub_ft + grammar decoder | 0.511 | 0.812 | 0.043 / 0.004 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug | 0.989 | 0.985 | 0.924 / 0.100 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug + grammar decoder | 0.990 | 0.987 | 0.957 / 0.103 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft | 0.987 | 0.950 | 0.913 / 0.097 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft + grammar decoder | 0.988 | 0.964 | 0.978 / 0.101 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_sub_ft | 0.988 | 0.956 | 0.935 / 0.101 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_sub_ft + grammar decoder | 0.989 | 0.964 | 0.967 / 0.098 | 92 |
