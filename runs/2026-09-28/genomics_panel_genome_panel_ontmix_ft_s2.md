# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_ontmix_ft_s2 | 0.979 | 0.973 | 0.466 / 0.435 | 0.898 / 0.839 | 0.914 / 0.899 | 0.691 / 0.562 | 0.411 / 0.110 | 0.975 | 0.952 | 0.262 / 0.171 | 0.891 | 0.149 | 0.940 |
| cjejuni (validation blocks) | genome_panel_ontmix_ft_s2 | 0.996 | 0.976 | 0.295 / 0.265 | 0.932 / 0.837 | 0.920 / 0.871 | 0.693 / 0.496 | 0.352 / 0.079 | 0.995 | 0.978 | 0.205 / 0.121 | 0.918 | 0.091 | 0.973 |
| cdifficile (validation blocks) | genome_panel_ontmix_ft_s2 | 0.992 | 0.987 | 0.480 / 0.440 | 0.960 / 0.881 | 0.954 / 0.914 | 0.688 / 0.567 | 0.384 / 0.097 | 0.990 | 0.971 | 0.306 / 0.194 | 0.913 | 0.162 | 0.961 |
| saureus (validation blocks) | genome_panel_ontmix_ft_s2 | 0.988 | 0.987 | 0.485 / 0.488 | 0.935 / 0.942 | 0.922 / 0.954 | 0.659 / 0.545 | 0.362 / 0.098 | 0.985 | 0.964 | 0.266 / 0.182 | 0.914 | 0.154 | 0.971 |
| hpylori (validation blocks) | genome_panel_ontmix_ft_s2 | 0.979 | 0.946 | 0.325 / 0.260 | 0.850 / 0.680 | 0.900 / 0.742 | 0.637 / 0.402 | 0.438 / 0.098 | 0.976 | 0.954 | 0.225 / 0.115 | 0.889 | 0.087 | 0.936 |
| lmonocytogenes (validation blocks) | genome_panel_ontmix_ft_s2 | 0.995 | 0.996 | 0.475 / 0.452 | 0.966 / 0.919 | 0.976 / 0.970 | 0.746 / 0.618 | 0.458 / 0.121 | 0.992 | 0.972 | 0.332 / 0.201 | 0.908 | 0.146 | 0.967 |
| vcholerae (validation blocks) | genome_panel_ontmix_ft_s2 | 0.990 | 0.995 | 0.546 / 0.509 | 0.940 / 0.876 | 0.964 / 0.949 | 0.747 / 0.565 | 0.418 / 0.094 | 0.987 | 0.967 | 0.373 / 0.221 | 0.902 | 0.177 | 0.957 |
| synechocystis (validation blocks) | genome_panel_ontmix_ft_s2 | 0.982 | 0.979 | 0.400 / 0.351 | 0.902 / 0.790 | 0.910 / 0.866 | 0.710 / 0.511 | 0.431 / 0.100 | 0.979 | 0.956 | 0.247 / 0.140 | 0.887 | 0.106 | 0.939 |
| styphimurium (validation blocks) | genome_panel_ontmix_ft_s2 | 0.980 | 0.986 | 0.490 / 0.431 | 0.922 / 0.811 | 0.956 / 0.905 | 0.732 / 0.586 | 0.355 / 0.089 | 0.976 | 0.952 | 0.279 / 0.185 | 0.884 | 0.120 | 0.933 |
| paeruginosa (validation blocks) | genome_panel_ontmix_ft_s2 | 0.994 | 0.988 | 0.741 / 0.680 | 0.980 / 0.900 | 0.986 / 0.935 | 0.809 / 0.743 | 0.428 / 0.109 | 0.993 | 0.988 | 0.565 / 0.489 | 0.949 | 0.265 | 0.980 |
| mtuberculosis (validation blocks) | genome_panel_ontmix_ft_s2 | 0.966 | 0.977 | 0.357 / 0.279 | 0.897 / 0.701 | 0.909 / 0.803 | 0.711 / 0.557 | 0.374 / 0.089 | 0.963 | 0.943 | 0.246 / 0.157 | 0.874 | 0.134 | 0.895 |
| scoelicolor (validation blocks) | genome_panel_ontmix_ft_s2 | 0.991 | 0.984 | 0.673 / 0.604 | 0.950 / 0.854 | 0.959 / 0.891 | 0.793 / 0.688 | 0.397 / 0.091 | 0.989 | 0.981 | 0.510 / 0.396 | 0.936 | 0.220 | 0.965 |
| mjannaschii (validation blocks) | genome_panel_ontmix_ft_s2 | 0.991 | 0.993 | 0.392 / 0.373 | 0.969 / 0.922 | 0.959 / 0.939 | 0.670 / 0.512 | 0.392 / 0.107 | 0.984 | 0.955 | 0.299 / 0.173 | 0.897 | 0.113 | 0.953 |
| bsubtilis (whole genome, held-out species) | genome_panel_ontmix_ft_s2 | 0.976 | 0.985 | 0.344 / 0.269 | 0.878 / 0.687 | 0.924 / 0.863 | 0.634 / 0.435 | 0.388 / 0.109 | 0.969 | 0.927 | 0.184 / 0.095 | 0.852 | 0.104 | 0.900 |
| spneumoniae (whole genome, held-out species) | genome_panel_ontmix_ft_s2 | 0.988 | 0.957 | 0.435 / 0.353 | 0.920 / 0.748 | 0.938 / 0.823 | 0.662 / 0.466 | 0.407 / 0.103 | 0.983 | 0.955 | 0.248 / 0.134 | 0.887 | 0.134 | 0.928 |
| dradiodurans (whole genome, held-out species) | genome_panel_ontmix_ft_s2 | 0.989 | 0.989 | 0.670 / 0.626 | 0.954 / 0.892 | 0.969 / 0.944 | 0.779 / 0.713 | 0.415 / 0.111 | 0.987 | 0.976 | 0.494 / 0.420 | 0.925 | 0.250 | 0.965 |
| tthermophilus (whole genome, held-out species) | genome_panel_ontmix_ft_s2 | 0.974 | 0.979 | 0.404 / 0.365 | 0.873 / 0.789 | 0.892 / 0.882 | 0.693 / 0.628 | 0.374 / 0.103 | 0.971 | 0.949 | 0.302 / 0.239 | 0.908 | 0.138 | 0.937 |
| hvolcanii (whole genome, held-out species) | genome_panel_ontmix_ft_s2 | 0.983 | 0.978 | 0.678 / 0.616 | 0.924 / 0.839 | 0.943 / 0.905 | 0.747 / 0.669 | 0.412 / 0.117 | 0.979 | 0.961 | 0.489 / 0.395 | 0.915 | 0.243 | 0.939 |
