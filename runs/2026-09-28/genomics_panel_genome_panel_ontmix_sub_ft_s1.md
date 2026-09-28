# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.983 | 0.973 | 0.487 / 0.463 | 0.893 / 0.848 | 0.903 / 0.898 | 0.712 / 0.675 | 0.414 / 0.110 | 0.981 | 0.966 | 0.317 / 0.264 | 0.893 | 0.170 | 0.939 |
| cjejuni (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.996 | 0.976 | 0.261 / 0.245 | 0.898 / 0.840 | 0.875 / 0.856 | 0.636 / 0.571 | 0.352 / 0.079 | 0.995 | 0.989 | 0.182 / 0.144 | 0.916 | 0.045 | 0.975 |
| cdifficile (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.994 | 0.987 | 0.434 / 0.409 | 0.934 / 0.880 | 0.908 / 0.865 | 0.685 / 0.641 | 0.384 / 0.096 | 0.993 | 0.983 | 0.275 / 0.226 | 0.912 | 0.130 | 0.963 |
| saureus (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.990 | 0.986 | 0.447 / 0.460 | 0.915 / 0.940 | 0.891 / 0.935 | 0.686 / 0.666 | 0.355 / 0.096 | 0.988 | 0.980 | 0.266 / 0.234 | 0.913 | 0.126 | 0.970 |
| hpylori (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.988 | 0.949 | 0.275 / 0.239 | 0.850 / 0.739 | 0.850 / 0.739 | 0.700 / 0.519 | 0.425 / 0.094 | 0.987 | 0.976 | 0.237 / 0.164 | 0.893 | 0.138 | 0.929 |
| lmonocytogenes (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.995 | 0.996 | 0.495 / 0.487 | 0.969 / 0.953 | 0.966 / 0.969 | 0.766 / 0.717 | 0.444 / 0.117 | 0.994 | 0.984 | 0.339 / 0.278 | 0.909 | 0.166 | 0.965 |
| vcholerae (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.991 | 0.994 | 0.498 / 0.479 | 0.944 / 0.907 | 0.944 / 0.944 | 0.747 / 0.660 | 0.418 / 0.094 | 0.989 | 0.979 | 0.361 / 0.278 | 0.901 | 0.173 | 0.957 |
| synechocystis (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.984 | 0.978 | 0.392 / 0.375 | 0.890 / 0.850 | 0.863 / 0.837 | 0.702 / 0.589 | 0.412 / 0.095 | 0.983 | 0.971 | 0.259 / 0.193 | 0.889 | 0.149 | 0.935 |
| styphimurium (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.984 | 0.986 | 0.450 / 0.418 | 0.922 / 0.856 | 0.940 / 0.902 | 0.738 / 0.673 | 0.357 / 0.090 | 0.981 | 0.967 | 0.319 / 0.253 | 0.888 | 0.133 | 0.935 |
| paeruginosa (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.994 | 0.988 | 0.728 / 0.686 | 0.979 / 0.922 | 0.977 / 0.932 | 0.805 / 0.761 | 0.440 / 0.112 | 0.993 | 0.989 | 0.581 / 0.535 | 0.950 | 0.265 | 0.980 |
| mtuberculosis (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.967 | 0.977 | 0.329 / 0.278 | 0.857 / 0.726 | 0.874 / 0.795 | 0.700 / 0.581 | 0.360 / 0.086 | 0.965 | 0.952 | 0.226 / 0.165 | 0.874 | 0.111 | 0.895 |
| scoelicolor (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.991 | 0.983 | 0.668 / 0.608 | 0.952 / 0.866 | 0.950 / 0.885 | 0.808 / 0.725 | 0.406 / 0.093 | 0.990 | 0.984 | 0.535 / 0.452 | 0.937 | 0.229 | 0.964 |
| mjannaschii (validation blocks) | genome_panel_ontmix_sub_ft_s1 | 0.991 | 0.993 | 0.381 / 0.366 | 0.959 / 0.921 | 0.938 / 0.919 | 0.691 / 0.609 | 0.381 / 0.104 | 0.988 | 0.970 | 0.330 / 0.244 | 0.895 | 0.103 | 0.948 |
| bsubtilis (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s1 | 0.980 | 0.985 | 0.335 / 0.287 | 0.887 / 0.762 | 0.914 / 0.871 | 0.657 / 0.534 | 0.385 / 0.108 | 0.976 | 0.951 | 0.206 / 0.133 | 0.854 | 0.107 | 0.899 |
| spneumoniae (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s1 | 0.989 | 0.955 | 0.415 / 0.354 | 0.912 / 0.777 | 0.906 / 0.807 | 0.670 / 0.542 | 0.399 / 0.101 | 0.986 | 0.971 | 0.258 / 0.183 | 0.888 | 0.136 | 0.929 |
| dradiodurans (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s1 | 0.990 | 0.989 | 0.644 / 0.610 | 0.954 / 0.904 | 0.959 / 0.936 | 0.789 / 0.756 | 0.419 / 0.112 | 0.988 | 0.981 | 0.492 / 0.446 | 0.925 | 0.242 | 0.963 |
| tthermophilus (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s1 | 0.976 | 0.980 | 0.354 / 0.332 | 0.867 / 0.812 | 0.883 / 0.886 | 0.720 / 0.697 | 0.373 / 0.102 | 0.975 | 0.964 | 0.289 / 0.254 | 0.914 | 0.122 | 0.924 |
| hvolcanii (whole genome, held-out species) | genome_panel_ontmix_sub_ft_s1 | 0.985 | 0.977 | 0.640 / 0.594 | 0.930 / 0.863 | 0.933 / 0.902 | 0.767 / 0.719 | 0.415 / 0.117 | 0.982 | 0.971 | 0.488 / 0.428 | 0.918 | 0.244 | 0.937 |
