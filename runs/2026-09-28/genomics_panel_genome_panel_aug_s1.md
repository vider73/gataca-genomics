# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_aug_s1 | 0.983 | 0.974 | 0.516 / 0.497 | 0.901 / 0.869 | 0.908 / 0.916 | 0.702 / 0.665 | 0.427 / 0.112 | 0.982 | 0.965 | 0.340 / 0.291 | 0.894 | 0.178 | 0.944 |
| cjejuni (validation blocks) | genome_panel_aug_s1 | 0.996 | 0.976 | 0.341 / 0.323 | 0.898 / 0.849 | 0.875 / 0.865 | 0.648 / 0.553 | 0.352 / 0.078 | 0.995 | 0.988 | 0.273 / 0.212 | 0.917 | 0.068 | 0.978 |
| cdifficile (validation blocks) | genome_panel_aug_s1 | 0.995 | 0.989 | 0.442 / 0.412 | 0.951 / 0.887 | 0.934 / 0.895 | 0.685 / 0.630 | 0.410 / 0.102 | 0.993 | 0.981 | 0.298 / 0.243 | 0.915 | 0.153 | 0.967 |
| saureus (validation blocks) | genome_panel_aug_s1 | 0.991 | 0.988 | 0.457 / 0.467 | 0.922 / 0.941 | 0.904 / 0.936 | 0.689 / 0.660 | 0.358 / 0.096 | 0.989 | 0.980 | 0.294 / 0.260 | 0.916 | 0.133 | 0.973 |
| hpylori (validation blocks) | genome_panel_aug_s1 | 0.988 | 0.950 | 0.312 / 0.269 | 0.850 / 0.731 | 0.863 / 0.742 | 0.662 / 0.520 | 0.438 / 0.096 | 0.988 | 0.975 | 0.237 / 0.165 | 0.895 | 0.138 | 0.934 |
| lmonocytogenes (validation blocks) | genome_panel_aug_s1 | 0.996 | 0.996 | 0.522 / 0.515 | 0.969 / 0.957 | 0.969 / 0.976 | 0.769 / 0.721 | 0.451 / 0.119 | 0.995 | 0.984 | 0.386 / 0.315 | 0.909 | 0.166 | 0.968 |
| vcholerae (validation blocks) | genome_panel_aug_s1 | 0.991 | 0.994 | 0.554 / 0.543 | 0.944 / 0.925 | 0.944 / 0.951 | 0.731 / 0.643 | 0.422 / 0.094 | 0.989 | 0.979 | 0.382 / 0.306 | 0.905 | 0.161 | 0.961 |
| synechocystis (validation blocks) | genome_panel_aug_s1 | 0.985 | 0.980 | 0.427 / 0.399 | 0.894 / 0.835 | 0.886 / 0.856 | 0.714 / 0.605 | 0.408 / 0.094 | 0.983 | 0.972 | 0.302 / 0.226 | 0.890 | 0.129 | 0.940 |
| styphimurium (validation blocks) | genome_panel_aug_s1 | 0.986 | 0.988 | 0.532 / 0.504 | 0.929 / 0.880 | 0.945 / 0.910 | 0.745 / 0.676 | 0.357 / 0.089 | 0.983 | 0.969 | 0.355 / 0.291 | 0.890 | 0.149 | 0.947 |
| paeruginosa (validation blocks) | genome_panel_aug_s1 | 0.995 | 0.989 | 0.760 / 0.715 | 0.986 / 0.928 | 0.977 / 0.933 | 0.812 / 0.764 | 0.429 / 0.108 | 0.994 | 0.990 | 0.608 / 0.563 | 0.951 | 0.281 | 0.981 |
| mtuberculosis (validation blocks) | genome_panel_aug_s1 | 0.969 | 0.978 | 0.377 / 0.328 | 0.880 / 0.766 | 0.880 / 0.808 | 0.697 / 0.600 | 0.371 / 0.088 | 0.967 | 0.956 | 0.263 / 0.204 | 0.877 | 0.123 | 0.901 |
| scoelicolor (validation blocks) | genome_panel_aug_s1 | 0.992 | 0.985 | 0.688 / 0.632 | 0.949 / 0.872 | 0.953 / 0.884 | 0.799 / 0.721 | 0.410 / 0.093 | 0.991 | 0.986 | 0.548 / 0.473 | 0.939 | 0.246 | 0.966 |
| mjannaschii (validation blocks) | genome_panel_aug_s1 | 0.992 | 0.994 | 0.495 / 0.480 | 0.959 / 0.930 | 0.948 / 0.929 | 0.670 / 0.580 | 0.402 / 0.108 | 0.988 | 0.968 | 0.361 / 0.267 | 0.897 | 0.113 | 0.956 |
| bsubtilis (whole genome, held-out species) | genome_panel_aug_s1 | 0.983 | 0.986 | 0.397 / 0.355 | 0.902 / 0.807 | 0.922 / 0.887 | 0.664 / 0.548 | 0.397 / 0.110 | 0.979 | 0.954 | 0.250 / 0.174 | 0.857 | 0.127 | 0.912 |
| spneumoniae (whole genome, held-out species) | genome_panel_aug_s1 | 0.990 | 0.957 | 0.465 / 0.405 | 0.925 / 0.806 | 0.915 / 0.816 | 0.668 / 0.549 | 0.411 / 0.103 | 0.987 | 0.971 | 0.301 / 0.220 | 0.890 | 0.148 | 0.936 |
| dradiodurans (whole genome, held-out species) | genome_panel_aug_s1 | 0.991 | 0.989 | 0.675 / 0.645 | 0.959 / 0.917 | 0.963 / 0.944 | 0.790 / 0.762 | 0.423 / 0.112 | 0.989 | 0.982 | 0.525 / 0.491 | 0.927 | 0.259 | 0.966 |
| tthermophilus (whole genome, held-out species) | genome_panel_aug_s1 | 0.981 | 0.982 | 0.398 / 0.386 | 0.885 / 0.858 | 0.894 / 0.904 | 0.721 / 0.709 | 0.375 / 0.102 | 0.980 | 0.970 | 0.327 / 0.303 | 0.913 | 0.139 | 0.934 |
| hvolcanii (whole genome, held-out species) | genome_panel_aug_s1 | 0.987 | 0.978 | 0.672 / 0.631 | 0.933 / 0.877 | 0.941 / 0.912 | 0.768 / 0.725 | 0.417 / 0.117 | 0.985 | 0.974 | 0.522 / 0.468 | 0.919 | 0.259 | 0.943 |
