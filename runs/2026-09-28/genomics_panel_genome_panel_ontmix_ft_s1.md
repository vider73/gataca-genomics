# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_ontmix_ft_s1 | 0.981 | 0.973 | 0.516 / 0.483 | 0.893 / 0.836 | 0.908 / 0.901 | 0.691 / 0.574 | 0.408 / 0.109 | 0.979 | 0.955 | 0.312 / 0.208 | 0.893 | 0.186 | 0.935 |
| cjejuni (validation blocks) | genome_panel_ontmix_ft_s1 | 0.996 | 0.976 | 0.364 / 0.323 | 0.920 / 0.818 | 0.898 / 0.840 | 0.682 / 0.484 | 0.352 / 0.078 | 0.994 | 0.979 | 0.273 / 0.161 | 0.918 | 0.080 | 0.970 |
| cdifficile (validation blocks) | genome_panel_ontmix_ft_s1 | 0.993 | 0.988 | 0.491 / 0.461 | 0.962 / 0.902 | 0.948 / 0.904 | 0.682 / 0.571 | 0.396 / 0.100 | 0.991 | 0.973 | 0.309 / 0.205 | 0.913 | 0.150 | 0.960 |
| saureus (validation blocks) | genome_panel_ontmix_ft_s1 | 0.989 | 0.987 | 0.498 / 0.503 | 0.928 / 0.938 | 0.922 / 0.957 | 0.683 / 0.585 | 0.358 / 0.097 | 0.986 | 0.969 | 0.300 / 0.210 | 0.914 | 0.140 | 0.968 |
| hpylori (validation blocks) | genome_panel_ontmix_ft_s1 | 0.985 | 0.950 | 0.287 / 0.219 | 0.887 / 0.676 | 0.900 / 0.791 | 0.688 / 0.447 | 0.425 / 0.094 | 0.983 | 0.961 | 0.200 / 0.103 | 0.893 | 0.113 | 0.921 |
| lmonocytogenes (validation blocks) | genome_panel_ontmix_ft_s1 | 0.995 | 0.996 | 0.519 / 0.494 | 0.973 / 0.926 | 0.966 / 0.973 | 0.756 / 0.626 | 0.454 / 0.120 | 0.992 | 0.973 | 0.376 / 0.237 | 0.909 | 0.163 | 0.963 |
| vcholerae (validation blocks) | genome_panel_ontmix_ft_s1 | 0.991 | 0.994 | 0.534 / 0.508 | 0.940 / 0.893 | 0.952 / 0.944 | 0.719 / 0.551 | 0.422 / 0.095 | 0.987 | 0.969 | 0.378 / 0.226 | 0.904 | 0.169 | 0.956 |
| synechocystis (validation blocks) | genome_panel_ontmix_ft_s1 | 0.983 | 0.980 | 0.443 / 0.401 | 0.898 / 0.812 | 0.910 / 0.866 | 0.710 / 0.534 | 0.431 / 0.100 | 0.980 | 0.956 | 0.267 / 0.163 | 0.889 | 0.137 | 0.933 |
| styphimurium (validation blocks) | genome_panel_ontmix_ft_s1 | 0.982 | 0.986 | 0.490 / 0.439 | 0.918 / 0.823 | 0.947 / 0.909 | 0.721 / 0.585 | 0.348 / 0.088 | 0.977 | 0.955 | 0.317 / 0.217 | 0.886 | 0.135 | 0.932 |
| paeruginosa (validation blocks) | genome_panel_ontmix_ft_s1 | 0.994 | 0.989 | 0.755 / 0.703 | 0.984 / 0.917 | 0.980 / 0.937 | 0.801 / 0.737 | 0.428 / 0.109 | 0.993 | 0.988 | 0.606 / 0.526 | 0.950 | 0.275 | 0.980 |
| mtuberculosis (validation blocks) | genome_panel_ontmix_ft_s1 | 0.967 | 0.978 | 0.357 / 0.299 | 0.891 / 0.746 | 0.911 / 0.822 | 0.691 / 0.549 | 0.371 / 0.088 | 0.964 | 0.944 | 0.277 / 0.192 | 0.874 | 0.120 | 0.893 |
| scoelicolor (validation blocks) | genome_panel_ontmix_ft_s1 | 0.990 | 0.984 | 0.691 / 0.627 | 0.956 / 0.867 | 0.959 / 0.897 | 0.796 / 0.677 | 0.409 / 0.094 | 0.988 | 0.980 | 0.532 / 0.410 | 0.936 | 0.240 | 0.961 |
| mjannaschii (validation blocks) | genome_panel_ontmix_ft_s1 | 0.991 | 0.994 | 0.474 / 0.447 | 0.959 / 0.903 | 0.959 / 0.949 | 0.680 / 0.512 | 0.381 / 0.105 | 0.987 | 0.957 | 0.330 / 0.203 | 0.899 | 0.124 | 0.949 |
| bsubtilis (whole genome, held-out species) | genome_panel_ontmix_ft_s1 | 0.978 | 0.985 | 0.375 / 0.303 | 0.889 / 0.717 | 0.925 / 0.870 | 0.638 / 0.448 | 0.390 / 0.110 | 0.972 | 0.932 | 0.217 / 0.117 | 0.853 | 0.115 | 0.891 |
| spneumoniae (whole genome, held-out species) | genome_panel_ontmix_ft_s1 | 0.988 | 0.957 | 0.481 / 0.393 | 0.930 / 0.761 | 0.933 / 0.820 | 0.671 / 0.475 | 0.409 / 0.103 | 0.984 | 0.958 | 0.270 / 0.153 | 0.888 | 0.149 | 0.923 |
| dradiodurans (whole genome, held-out species) | genome_panel_ontmix_ft_s1 | 0.990 | 0.989 | 0.678 / 0.640 | 0.957 / 0.904 | 0.967 / 0.941 | 0.777 / 0.712 | 0.418 / 0.112 | 0.987 | 0.977 | 0.509 / 0.433 | 0.926 | 0.256 | 0.962 |
| tthermophilus (whole genome, held-out species) | genome_panel_ontmix_ft_s1 | 0.976 | 0.980 | 0.402 / 0.365 | 0.883 / 0.800 | 0.906 / 0.890 | 0.703 / 0.641 | 0.369 / 0.101 | 0.972 | 0.956 | 0.313 / 0.249 | 0.909 | 0.135 | 0.920 |
| hvolcanii (whole genome, held-out species) | genome_panel_ontmix_ft_s1 | 0.984 | 0.978 | 0.691 / 0.634 | 0.932 / 0.855 | 0.947 / 0.910 | 0.751 / 0.678 | 0.412 / 0.117 | 0.981 | 0.966 | 0.503 / 0.415 | 0.916 | 0.259 | 0.934 |
