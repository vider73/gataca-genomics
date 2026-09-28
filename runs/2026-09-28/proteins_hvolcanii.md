# Proteins recovered from raw nanopore reads — hvolcanii

Each read on its own. diamond_self uses the held-out genome's own proteome: an oracle, not a fair method.

| run | read identity | method | genes recovered (>=80% cov & id) | mean id x cov | precision | proteins predicted | genes in reads |
|---|---|---|---|---|---|---|---|
| ERR17000570 | 96.3% | diamond_panel | 0.259 | 0.299 | 0.948 | 1627 | 3811 |
| ERR17000570 | 96.3% | diamond_self | 0.963 | 0.942 | 0.974 | 4213 | 3811 |
| ERR17000570 | 96.3% | fgs_454_10 | 0.864 | 0.867 | 0.833 | 3341 | 3811 |
| ERR17000570 | 96.3% | fgs_454_30 | 0.853 | 0.854 | 0.811 | 3058 | 3811 |
| ERR17000570 | 96.3% | fgs_sanger_10 | 0.857 | 0.867 | 0.850 | 3545 | 3811 |
| ERR17000570 | 96.3% | genome_panel_aug | 0.856 | 0.864 | 0.903 | 3745 | 3811 |
| ERR17000570 | 96.3% | genome_panel_aug+decoder | 0.883 | 0.884 | 0.906 | 3744 | 3811 |
| ERR17000570 | 96.3% | genome_panel_aug_s1 | 0.858 | 0.866 | 0.898 | 3724 | 3811 |
| ERR17000570 | 96.3% | genome_panel_aug_s1+decoder | 0.888 | 0.886 | 0.900 | 3746 | 3811 |
| ERR17000570 | 96.3% | genome_panel_aug_s2 | 0.854 | 0.861 | 0.903 | 3761 | 3811 |
| ERR17000570 | 96.3% | genome_panel_aug_s2+decoder | 0.882 | 0.883 | 0.903 | 3748 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_ft | 0.834 | 0.853 | 0.899 | 3821 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_ft+decoder | 0.871 | 0.879 | 0.905 | 3836 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_ft_s1 | 0.837 | 0.855 | 0.895 | 3792 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_ft_s1+decoder | 0.872 | 0.879 | 0.897 | 3811 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_ft_s2 | 0.832 | 0.850 | 0.899 | 3836 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_ft_s2+decoder | 0.867 | 0.877 | 0.898 | 3821 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_sub_ft | 0.851 | 0.863 | 0.900 | 3759 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_sub_ft+decoder | 0.879 | 0.883 | 0.903 | 3754 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_sub_ft_s1 | 0.846 | 0.860 | 0.896 | 3752 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_sub_ft_s1+decoder | 0.877 | 0.881 | 0.896 | 3753 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_sub_ft_s2 | 0.853 | 0.861 | 0.895 | 3765 | 3811 |
| ERR17000570 | 96.3% | genome_panel_ontmix_sub_ft_s2+decoder | 0.880 | 0.884 | 0.897 | 3760 | 3811 |
| ERR17000570 | 96.3% | prodigal | 0.257 | 0.518 | 0.699 | 5716 | 3811 |
| SRR11991309 | 82.2% | diamond_panel | 0.000 | 0.002 | 0.053 | 19 | 92 |
| SRR11991309 | 82.2% | diamond_self | 0.022 | 0.285 | 0.032 | 537 | 92 |
| SRR11991309 | 82.2% | fgs_454_10 | 0.000 | 0.205 | 0.004 | 1579 | 92 |
| SRR11991309 | 82.2% | fgs_454_30 | 0.000 | 0.241 | 0.006 | 1412 | 92 |
| SRR11991309 | 82.2% | fgs_sanger_10 | 0.000 | 0.166 | 0.006 | 1579 | 92 |
| SRR11991309 | 82.2% | genome_panel_aug | 0.000 | 0.136 | 0.019 | 953 | 92 |
| SRR11991309 | 82.2% | genome_panel_aug+decoder | 0.000 | 0.141 | 0.019 | 1135 | 92 |
| SRR11991309 | 82.2% | genome_panel_aug_s1 | 0.000 | 0.157 | 0.013 | 1001 | 92 |
| SRR11991309 | 82.2% | genome_panel_aug_s1+decoder | 0.000 | 0.157 | 0.015 | 1228 | 92 |
| SRR11991309 | 82.2% | genome_panel_aug_s2 | 0.000 | 0.120 | 0.025 | 970 | 92 |
| SRR11991309 | 82.2% | genome_panel_aug_s2+decoder | 0.000 | 0.153 | 0.016 | 1169 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_ft | 0.000 | 0.253 | 0.008 | 1310 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_ft+decoder | 0.000 | 0.252 | 0.006 | 1562 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_ft_s1 | 0.000 | 0.248 | 0.006 | 1269 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_ft_s1+decoder | 0.000 | 0.240 | 0.009 | 1527 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_ft_s2 | 0.000 | 0.249 | 0.006 | 1281 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_ft_s2+decoder | 0.000 | 0.251 | 0.010 | 1527 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_sub_ft | 0.000 | 0.248 | 0.010 | 1246 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_sub_ft+decoder | 0.000 | 0.245 | 0.006 | 1480 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_sub_ft_s1 | 0.000 | 0.254 | 0.007 | 1216 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_sub_ft_s1+decoder | 0.000 | 0.269 | 0.010 | 1508 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_sub_ft_s2 | 0.000 | 0.246 | 0.009 | 1270 | 92 |
| SRR11991309 | 82.2% | genome_panel_ontmix_sub_ft_s2+decoder | 0.000 | 0.235 | 0.008 | 1543 | 92 |
| SRR11991309 | 82.2% | prodigal | 0.000 | 0.033 | 0.009 | 1134 | 92 |
