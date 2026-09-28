# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_aug_s2 | 0.983 | 0.975 | 0.455 / 0.438 | 0.906 / 0.872 | 0.916 / 0.919 | 0.709 / 0.663 | 0.427 / 0.113 | 0.982 | 0.967 | 0.304 / 0.252 | 0.895 | 0.178 | 0.947 |
| cjejuni (validation blocks) | genome_panel_aug_s2 | 0.996 | 0.976 | 0.330 / 0.315 | 0.909 / 0.870 | 0.898 / 0.868 | 0.682 / 0.566 | 0.364 / 0.081 | 0.995 | 0.988 | 0.239 / 0.186 | 0.918 | 0.091 | 0.980 |
| cdifficile (validation blocks) | genome_panel_aug_s2 | 0.994 | 0.988 | 0.468 / 0.439 | 0.954 / 0.894 | 0.934 / 0.897 | 0.694 / 0.640 | 0.399 / 0.099 | 0.993 | 0.981 | 0.292 / 0.243 | 0.915 | 0.171 | 0.965 |
| saureus (validation blocks) | genome_panel_aug_s2 | 0.990 | 0.988 | 0.464 / 0.474 | 0.925 / 0.944 | 0.904 / 0.950 | 0.686 / 0.661 | 0.362 / 0.097 | 0.988 | 0.978 | 0.280 / 0.240 | 0.915 | 0.147 | 0.974 |
| hpylori (validation blocks) | genome_panel_aug_s2 | 0.987 | 0.949 | 0.237 / 0.209 | 0.850 / 0.747 | 0.850 / 0.723 | 0.675 / 0.519 | 0.438 / 0.096 | 0.986 | 0.975 | 0.225 / 0.173 | 0.897 | 0.075 | 0.942 |
| lmonocytogenes (validation blocks) | genome_panel_aug_s2 | 0.996 | 0.996 | 0.454 / 0.448 | 0.963 / 0.950 | 0.966 / 0.969 | 0.753 / 0.698 | 0.454 / 0.120 | 0.994 | 0.983 | 0.325 / 0.260 | 0.908 | 0.146 | 0.972 |
| vcholerae (validation blocks) | genome_panel_aug_s2 | 0.991 | 0.994 | 0.550 / 0.535 | 0.936 / 0.910 | 0.940 / 0.951 | 0.755 / 0.657 | 0.414 / 0.092 | 0.989 | 0.979 | 0.386 / 0.297 | 0.903 | 0.181 | 0.964 |
| synechocystis (validation blocks) | genome_panel_aug_s2 | 0.986 | 0.979 | 0.439 / 0.407 | 0.894 / 0.829 | 0.882 / 0.836 | 0.702 / 0.581 | 0.416 / 0.095 | 0.984 | 0.971 | 0.286 / 0.209 | 0.889 | 0.122 | 0.945 |
| styphimurium (validation blocks) | genome_panel_aug_s2 | 0.985 | 0.987 | 0.521 / 0.490 | 0.933 / 0.877 | 0.958 / 0.911 | 0.749 / 0.664 | 0.368 / 0.091 | 0.982 | 0.966 | 0.346 / 0.284 | 0.889 | 0.131 | 0.945 |
| paeruginosa (validation blocks) | genome_panel_aug_s2 | 0.994 | 0.988 | 0.753 / 0.704 | 0.977 / 0.913 | 0.980 / 0.935 | 0.814 / 0.771 | 0.435 / 0.110 | 0.994 | 0.990 | 0.597 / 0.556 | 0.949 | 0.275 | 0.981 |
| mtuberculosis (validation blocks) | genome_panel_aug_s2 | 0.970 | 0.977 | 0.354 / 0.305 | 0.883 / 0.759 | 0.891 / 0.808 | 0.703 / 0.587 | 0.374 / 0.088 | 0.968 | 0.954 | 0.257 / 0.200 | 0.876 | 0.143 | 0.902 |
| scoelicolor (validation blocks) | genome_panel_aug_s2 | 0.992 | 0.984 | 0.661 / 0.610 | 0.949 / 0.876 | 0.950 / 0.882 | 0.799 / 0.729 | 0.407 / 0.092 | 0.990 | 0.985 | 0.525 / 0.449 | 0.939 | 0.226 | 0.968 |
| mjannaschii (validation blocks) | genome_panel_aug_s2 | 0.992 | 0.993 | 0.412 / 0.404 | 0.959 / 0.939 | 0.959 / 0.949 | 0.660 / 0.587 | 0.392 / 0.107 | 0.989 | 0.968 | 0.330 / 0.235 | 0.896 | 0.103 | 0.959 |
| bsubtilis (whole genome, held-out species) | genome_panel_aug_s2 | 0.982 | 0.986 | 0.361 / 0.322 | 0.897 / 0.801 | 0.916 / 0.885 | 0.655 / 0.542 | 0.397 / 0.110 | 0.979 | 0.954 | 0.216 / 0.147 | 0.857 | 0.117 | 0.917 |
| spneumoniae (whole genome, held-out species) | genome_panel_aug_s2 | 0.990 | 0.957 | 0.430 / 0.372 | 0.924 / 0.799 | 0.919 / 0.819 | 0.675 / 0.549 | 0.408 / 0.102 | 0.987 | 0.971 | 0.276 / 0.198 | 0.892 | 0.148 | 0.940 |
| dradiodurans (whole genome, held-out species) | genome_panel_aug_s2 | 0.990 | 0.989 | 0.682 / 0.651 | 0.956 / 0.913 | 0.961 / 0.941 | 0.794 / 0.768 | 0.421 / 0.112 | 0.989 | 0.982 | 0.523 / 0.485 | 0.927 | 0.261 | 0.967 |
| tthermophilus (whole genome, held-out species) | genome_panel_aug_s2 | 0.984 | 0.983 | 0.396 / 0.381 | 0.890 / 0.857 | 0.887 / 0.904 | 0.720 / 0.713 | 0.379 / 0.103 | 0.982 | 0.972 | 0.333 / 0.307 | 0.915 | 0.150 | 0.950 |
| hvolcanii (whole genome, held-out species) | genome_panel_aug_s2 | 0.987 | 0.978 | 0.664 / 0.615 | 0.932 / 0.864 | 0.941 / 0.911 | 0.767 / 0.719 | 0.414 / 0.117 | 0.984 | 0.972 | 0.497 / 0.437 | 0.918 | 0.249 | 0.946 |
