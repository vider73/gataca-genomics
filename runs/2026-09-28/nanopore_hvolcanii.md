# Real nanopore reads — hvolcanii (held-out species)

reads = the real reads; clean = the same reference stretches without sequencing errors.
Each read is processed on its own. Prodigal runs in metagenomic mode.

| run | read identity | input | target | frame acc | coding F1 | genes sens / prec (exact stop) | genes in reads |
|---|---|---|---|---|---|---|---|
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft | 0.943 | 0.974 | 0.590 / 0.220 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft + grammar decoder | 0.946 | 0.974 | 0.614 / 0.224 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft | 0.986 | 0.980 | 0.934 / 0.793 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft + grammar decoder | 0.988 | 0.981 | 0.949 / 0.841 | 3811 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft | 0.542 | 0.793 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft + grammar decoder | 0.530 | 0.794 | 0.022 / 0.003 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft | 0.987 | 0.950 | 0.913 / 0.097 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft + grammar decoder | 0.988 | 0.964 | 0.978 / 0.101 | 92 |
