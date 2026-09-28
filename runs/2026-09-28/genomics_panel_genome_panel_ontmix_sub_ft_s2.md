# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.984 | 0.975 | 0.432 / 0.411 | 0.901 / 0.858 | 0.916 / 0.921 | 0.717 / 0.680 | 0.424 / 0.112 | 0.982 | 0.968 | 0.285 / 0.230 | 0.894 | 0.168 | 0.947 |
| cjejuni (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.996 | 0.976 | 0.227 / 0.215 | 0.898 / 0.849 | 0.886 / 0.857 | 0.659 / 0.574 | 0.386 / 0.086 | 0.995 | 0.989 | 0.193 / 0.150 | 0.915 | 0.045 | 0.979 |
| cdifficile (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.993 | 0.987 | 0.425 / 0.393 | 0.945 / 0.874 | 0.919 / 0.878 | 0.685 / 0.625 | 0.396 / 0.099 | 0.991 | 0.980 | 0.272 / 0.222 | 0.912 | 0.147 | 0.964 |
| saureus (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.989 | 0.986 | 0.437 / 0.441 | 0.925 / 0.934 | 0.904 / 0.943 | 0.676 / 0.639 | 0.355 / 0.096 | 0.988 | 0.978 | 0.270 / 0.233 | 0.914 | 0.143 | 0.975 |
| hpylori (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.986 | 0.949 | 0.263 / 0.226 | 0.812 / 0.699 | 0.850 / 0.723 | 0.675 / 0.500 | 0.438 / 0.097 | 0.985 | 0.975 | 0.200 / 0.133 | 0.896 | 0.087 | 0.944 |
| lmonocytogenes (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.995 | 0.996 | 0.427 / 0.417 | 0.963 / 0.940 | 0.963 / 0.969 | 0.749 / 0.706 | 0.461 / 0.123 | 0.994 | 0.982 | 0.332 / 0.267 | 0.907 | 0.129 | 0.970 |
| vcholerae (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.991 | 0.994 | 0.522 / 0.506 | 0.936 / 0.907 | 0.940 / 0.951 | 0.759 / 0.680 | 0.418 / 0.095 | 0.989 | 0.979 | 0.386 / 0.296 | 0.902 | 0.169 | 0.960 |
| synechocystis (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.986 | 0.979 | 0.408 / 0.374 | 0.902 / 0.827 | 0.875 / 0.845 | 0.682 / 0.578 | 0.424 / 0.098 | 0.985 | 0.972 | 0.235 / 0.166 | 0.888 | 0.090 | 0.943 |
| styphimurium (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.985 | 0.987 | 0.497 / 0.460 | 0.918 / 0.850 | 0.945 / 0.901 | 0.743 / 0.653 | 0.353 / 0.088 | 0.981 | 0.967 | 0.306 / 0.247 | 0.886 | 0.124 | 0.937 |
| paeruginosa (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.995 | 0.988 | 0.742 / 0.699 | 0.975 / 0.918 | 0.979 / 0.935 | 0.816 / 0.770 | 0.436 / 0.111 | 0.994 | 0.990 | 0.585 / 0.545 | 0.949 | 0.270 | 0.982 |
| mtuberculosis (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.968 | 0.975 | 0.326 / 0.270 | 0.880 / 0.728 | 0.880 / 0.790 | 0.703 / 0.575 | 0.357 / 0.085 | 0.967 | 0.953 | 0.223 / 0.165 | 0.875 | 0.114 | 0.898 |
| scoelicolor (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.991 | 0.983 | 0.643 / 0.588 | 0.953 / 0.872 | 0.956 / 0.890 | 0.801 / 0.723 | 0.400 / 0.091 | 0.990 | 0.985 | 0.505 / 0.430 | 0.937 | 0.214 | 0.966 |
| mjannaschii (validation blocks) | genome_panel_ontmix_sub_ft_s2 | 0.991 | 0.992 | 0.371 / 0.360 | 0.959 / 0.930 | 0.938 / 0.938 | 0.680 / 0.611 | 0.392 / 0.109 | 0.987 | 0.971 | 0.340 / 0.244 | 0.895 | 0.082 | 0.953 |
| bsubtilis (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s2 | 0.979 | 0.985 | 0.325 / 0.276 | 0.883 / 0.750 | 0.912 / 0.875 | 0.657 / 0.531 | 0.389 / 0.109 | 0.975 | 0.949 | 0.188 / 0.120 | 0.853 | 0.096 | 0.906 |
| spneumoniae (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s2 | 0.989 | 0.956 | 0.400 / 0.340 | 0.917 / 0.778 | 0.915 / 0.811 | 0.676 / 0.545 | 0.402 / 0.102 | 0.986 | 0.970 | 0.249 / 0.174 | 0.890 | 0.135 | 0.936 |
| dradiodurans (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s2 | 0.991 | 0.989 | 0.656 / 0.625 | 0.954 / 0.910 | 0.963 / 0.942 | 0.794 / 0.767 | 0.419 / 0.111 | 0.989 | 0.982 | 0.500 / 0.460 | 0.926 | 0.245 | 0.966 |
| tthermophilus (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s2 | 0.982 | 0.982 | 0.378 / 0.357 | 0.879 / 0.830 | 0.881 / 0.900 | 0.722 / 0.715 | 0.375 / 0.101 | 0.980 | 0.971 | 0.306 / 0.272 | 0.921 | 0.133 | 0.948 |
| hvolcanii (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s2 | 0.986 | 0.977 | 0.654 / 0.609 | 0.927 / 0.863 | 0.936 / 0.908 | 0.768 / 0.725 | 0.413 / 0.117 | 0.984 | 0.972 | 0.487 / 0.431 | 0.918 | 0.241 | 0.943 |
