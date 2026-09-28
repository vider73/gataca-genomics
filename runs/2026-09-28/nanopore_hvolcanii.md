# Real nanopore reads — hvolcanii (held-out species)

reads = the real reads; clean = the same reference stretches without sequencing errors.
Each read is processed on its own. Prodigal runs in metagenomic mode.

| run | read identity | input | target | frame acc | coding F1 | genes sens / prec (exact stop) | genes in reads |
|---|---|---|---|---|---|---|---|
| ERR17000570 | 96.3% | reads | genome_panel_aug_s1 | 0.946 | 0.974 | 0.599 / 0.219 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_aug_s1 + grammar decoder | 0.947 | 0.974 | 0.612 / 0.221 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_aug_s2 | 0.945 | 0.974 | 0.598 / 0.219 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_aug_s2 + grammar decoder | 0.947 | 0.975 | 0.612 / 0.221 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft_s1 | 0.943 | 0.974 | 0.592 / 0.220 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft_s1 + grammar decoder | 0.946 | 0.974 | 0.613 / 0.223 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft_s2 | 0.943 | 0.974 | 0.589 / 0.219 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_ft_s2 + grammar decoder | 0.945 | 0.975 | 0.613 / 0.223 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_sub_ft_s1 | 0.945 | 0.973 | 0.592 / 0.219 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_sub_ft_s1 + grammar decoder | 0.946 | 0.974 | 0.606 / 0.220 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_sub_ft_s2 | 0.946 | 0.974 | 0.592 / 0.219 | 3811 |
| ERR17000570 | 96.3% | reads | genome_panel_ontmix_sub_ft_s2 + grammar decoder | 0.948 | 0.975 | 0.610 / 0.221 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug_s1 | 0.989 | 0.980 | 0.940 / 0.811 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug_s1 + grammar decoder | 0.990 | 0.981 | 0.944 / 0.837 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug_s2 | 0.988 | 0.980 | 0.936 / 0.805 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_aug_s2 + grammar decoder | 0.990 | 0.981 | 0.944 / 0.836 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft_s1 | 0.987 | 0.980 | 0.936 / 0.795 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft_s1 + grammar decoder | 0.988 | 0.981 | 0.951 / 0.837 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft_s2 | 0.986 | 0.980 | 0.932 / 0.786 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_ft_s2 + grammar decoder | 0.988 | 0.981 | 0.951 / 0.834 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_sub_ft_s1 | 0.987 | 0.979 | 0.936 / 0.802 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_sub_ft_s1 + grammar decoder | 0.989 | 0.980 | 0.938 / 0.832 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_sub_ft_s2 | 0.988 | 0.980 | 0.934 / 0.801 | 3811 |
| ERR17000570 | 96.3% | clean | genome_panel_ontmix_sub_ft_s2 + grammar decoder | 0.990 | 0.981 | 0.943 / 0.834 | 3811 |
| SRR11991309 | 82.2% | reads | genome_panel_aug_s1 | 0.403 | 0.734 | 0.022 / 0.003 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_aug_s1 + grammar decoder | 0.382 | 0.725 | 0.022 / 0.002 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_aug_s2 | 0.370 | 0.693 | 0.022 / 0.003 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_aug_s2 + grammar decoder | 0.350 | 0.680 | 0.022 / 0.002 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft_s1 | 0.537 | 0.796 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft_s1 + grammar decoder | 0.510 | 0.795 | 0.022 / 0.002 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft_s2 | 0.527 | 0.789 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_ft_s2 + grammar decoder | 0.503 | 0.789 | 0.033 / 0.003 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_sub_ft_s1 | 0.544 | 0.808 | 0.000 / 0.000 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_sub_ft_s1 + grammar decoder | 0.519 | 0.810 | 0.022 / 0.002 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_sub_ft_s2 | 0.526 | 0.786 | 0.011 / 0.003 | 92 |
| SRR11991309 | 82.2% | reads | genome_panel_ontmix_sub_ft_s2 + grammar decoder | 0.500 | 0.787 | 0.043 / 0.004 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug_s1 | 0.991 | 0.886 | 0.946 / 0.062 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug_s1 + grammar decoder | 0.992 | 0.893 | 0.978 / 0.059 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug_s2 | 0.989 | 0.904 | 0.946 / 0.076 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_aug_s2 + grammar decoder | 0.990 | 0.909 | 0.967 / 0.062 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft_s1 | 0.988 | 0.870 | 0.935 / 0.100 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft_s1 + grammar decoder | 0.990 | 0.883 | 0.957 / 0.068 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft_s2 | 0.988 | 0.873 | 0.957 / 0.104 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_ft_s2 + grammar decoder | 0.989 | 0.914 | 0.967 / 0.100 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_sub_ft_s1 | 0.989 | 0.947 | 0.924 / 0.099 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_sub_ft_s1 + grammar decoder | 0.991 | 0.969 | 0.989 / 0.102 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_sub_ft_s2 | 0.990 | 0.820 | 0.935 / 0.102 | 92 |
| SRR11991309 | 82.2% | clean | genome_panel_ontmix_sub_ft_s2 + grammar decoder | 0.992 | 0.839 | 0.978 / 0.078 | 92 |
