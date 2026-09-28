# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | genes grammar decoder | decoder sub 5% | decoder indel 1% | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | genome_panel_ontmix_ft | 0.978 | 0.972 | 0.503 / 0.473 | 0.882 / 0.830 | 0.911 / 0.885 | 0.696 / 0.576 | 0.395 / 0.106 | 0.975 | 0.954 | 0.293 / 0.188 | 0.891 | 0.178 | 0.937 |
| ecoli (validation blocks) | prodigal | 0.991 | 0.978 | 0.953 / 0.945 | — | — | — | — | 0.966 | 0.846 | 0.592 / 0.329 | 0.528 | — | 0.902 |
| ecoli (validation blocks) | orf | 0.918 | 0.950 | 0.798 / 0.944 | — | — | — | — | 0.841 | 0.598 | 0.317 / 0.311 | 0.219 | — | 0.593 |
| cjejuni (validation blocks) | genome_panel_ontmix_ft | 0.995 | 0.976 | 0.341 / 0.316 | 0.920 / 0.853 | 0.898 / 0.859 | 0.693 / 0.480 | 0.364 / 0.080 | 0.994 | 0.979 | 0.227 / 0.136 | 0.918 | 0.057 | 0.974 |
| cjejuni (validation blocks) | prodigal | 0.998 | 0.983 | 1.000 / 0.917 | — | — | — | — | 0.960 | 0.797 | 0.602 / 0.265 | 0.567 | — | 0.947 |
| cjejuni (validation blocks) | orf | 0.944 | 0.960 | 0.886 / 0.951 | — | — | — | — | 0.849 | 0.543 | 0.273 / 0.258 | 0.175 | — | 0.774 |
| cdifficile (validation blocks) | genome_panel_ontmix_ft | 0.993 | 0.987 | 0.523 / 0.485 | 0.954 / 0.885 | 0.951 / 0.901 | 0.691 / 0.564 | 0.390 / 0.098 | 0.991 | 0.971 | 0.318 / 0.202 | 0.916 | 0.173 | 0.962 |
| cdifficile (validation blocks) | prodigal | 0.998 | 0.995 | 0.994 / 0.980 | — | — | — | — | 0.945 | 0.779 | 0.512 / 0.247 | 0.522 | — | 0.918 |
| cdifficile (validation blocks) | orf | 0.955 | 0.974 | 0.905 / 0.975 | — | — | — | — | 0.845 | 0.495 | 0.269 / 0.299 | 0.151 | — | 0.766 |
| saureus (validation blocks) | genome_panel_ontmix_ft | 0.989 | 0.986 | 0.543 / 0.548 | 0.932 / 0.941 | 0.922 / 0.954 | 0.666 / 0.557 | 0.355 / 0.096 | 0.986 | 0.967 | 0.324 / 0.225 | 0.915 | 0.164 | 0.969 |
| saureus (validation blocks) | prodigal | 0.992 | 0.991 | 0.956 / 0.982 | — | — | — | — | 0.944 | 0.783 | 0.495 / 0.253 | 0.521 | — | 0.931 |
| saureus (validation blocks) | orf | 0.953 | 0.971 | 0.857 / 0.984 | — | — | — | — | 0.839 | 0.496 | 0.263 / 0.307 | 0.135 | — | 0.769 |
| hpylori (validation blocks) | genome_panel_ontmix_ft | 0.985 | 0.949 | 0.275 / 0.222 | 0.887 / 0.717 | 0.887 / 0.772 | 0.713 / 0.456 | 0.450 / 0.100 | 0.983 | 0.963 | 0.225 / 0.121 | 0.897 | 0.100 | 0.928 |
| hpylori (validation blocks) | prodigal | 0.993 | 0.962 | 0.988 / 0.888 | — | — | — | — | 0.964 | 0.854 | 0.662 / 0.283 | 0.579 | — | 0.899 |
| hpylori (validation blocks) | orf | 0.943 | 0.945 | 0.875 / 0.909 | — | — | — | — | 0.824 | 0.542 | 0.300 / 0.300 | 0.158 | — | 0.760 |
| lmonocytogenes (validation blocks) | genome_panel_ontmix_ft | 0.994 | 0.996 | 0.536 / 0.506 | 0.973 / 0.920 | 0.976 / 0.973 | 0.739 / 0.602 | 0.461 / 0.122 | 0.991 | 0.972 | 0.373 / 0.238 | 0.908 | 0.166 | 0.965 |
| lmonocytogenes (validation blocks) | prodigal | 0.999 | 0.998 | 1.000 / 0.990 | — | — | — | — | 0.965 | 0.836 | 0.597 / 0.318 | 0.548 | — | 0.921 |
| lmonocytogenes (validation blocks) | orf | 0.949 | 0.973 | 0.919 / 0.996 | — | — | — | — | 0.880 | 0.584 | 0.336 / 0.331 | 0.190 | — | 0.780 |
| vcholerae (validation blocks) | genome_panel_ontmix_ft | 0.990 | 0.994 | 0.550 / 0.515 | 0.936 / 0.876 | 0.956 / 0.944 | 0.747 / 0.565 | 0.422 / 0.095 | 0.987 | 0.969 | 0.402 / 0.242 | 0.903 | 0.189 | 0.956 |
| vcholerae (validation blocks) | prodigal | 0.997 | 0.996 | 0.988 / 0.976 | — | — | — | — | 0.968 | 0.869 | 0.618 / 0.302 | 0.561 | — | 0.920 |
| vcholerae (validation blocks) | orf | 0.950 | 0.975 | 0.896 / 0.982 | — | — | — | — | 0.876 | 0.642 | 0.369 / 0.306 | 0.192 | — | 0.734 |
| synechocystis (validation blocks) | genome_panel_ontmix_ft | 0.981 | 0.978 | 0.475 / 0.432 | 0.902 / 0.821 | 0.922 / 0.864 | 0.682 / 0.513 | 0.439 / 0.101 | 0.977 | 0.956 | 0.271 / 0.159 | 0.888 | 0.141 | 0.932 |
| synechocystis (validation blocks) | prodigal | 0.994 | 0.991 | 0.984 / 0.958 | — | — | — | — | 0.963 | 0.868 | 0.663 / 0.313 | 0.553 | — | 0.878 |
| synechocystis (validation blocks) | orf | 0.939 | 0.965 | 0.824 / 0.981 | — | — | — | — | 0.828 | 0.549 | 0.333 / 0.336 | 0.172 | — | 0.687 |
| styphimurium (validation blocks) | genome_panel_ontmix_ft | 0.984 | 0.987 | 0.503 / 0.444 | 0.916 / 0.808 | 0.949 / 0.895 | 0.723 / 0.571 | 0.361 / 0.090 | 0.979 | 0.956 | 0.335 / 0.224 | 0.890 | 0.153 | 0.936 |
| styphimurium (validation blocks) | prodigal | 0.992 | 0.992 | 0.978 / 0.965 | — | — | — | — | 0.957 | 0.853 | 0.630 / 0.335 | 0.528 | — | 0.887 |
| styphimurium (validation blocks) | orf | 0.938 | 0.972 | 0.858 / 0.972 | — | — | — | — | 0.864 | 0.610 | 0.368 / 0.330 | 0.218 | — | 0.538 |
| paeruginosa (validation blocks) | genome_panel_ontmix_ft | 0.994 | 0.989 | 0.778 / 0.726 | 0.982 / 0.917 | 0.987 / 0.937 | 0.816 / 0.744 | 0.424 / 0.108 | 0.993 | 0.989 | 0.610 / 0.526 | 0.950 | 0.284 | 0.979 |
| paeruginosa (validation blocks) | prodigal | 0.996 | 0.993 | 0.998 / 0.969 | — | — | — | — | 0.975 | 0.907 | 0.719 / 0.414 | 0.474 | — | 0.950 |
| paeruginosa (validation blocks) | orf | 0.511 | 0.923 | 0.463 / 0.569 | — | — | — | — | 0.498 | 0.439 | 0.250 / 0.242 | 0.255 | — | 0.208 |
| mtuberculosis (validation blocks) | genome_panel_ontmix_ft | 0.967 | 0.977 | 0.383 / 0.308 | 0.886 / 0.713 | 0.917 / 0.819 | 0.697 / 0.565 | 0.371 / 0.088 | 0.964 | 0.945 | 0.277 / 0.189 | 0.876 | 0.146 | 0.893 |
| mtuberculosis (validation blocks) | prodigal | 0.983 | 0.981 | 0.986 / 0.943 | — | — | — | — | 0.954 | 0.877 | 0.660 / 0.370 | 0.482 | — | 0.863 |
| mtuberculosis (validation blocks) | orf | 0.820 | 0.933 | 0.726 / 0.794 | — | — | — | — | 0.776 | 0.575 | 0.334 / 0.290 | 0.242 | — | 0.403 |
| scoelicolor (validation blocks) | genome_panel_ontmix_ft | 0.990 | 0.984 | 0.701 / 0.631 | 0.958 / 0.862 | 0.959 / 0.887 | 0.789 / 0.682 | 0.401 / 0.092 | 0.989 | 0.981 | 0.526 / 0.412 | 0.936 | 0.235 | 0.962 |
| scoelicolor (validation blocks) | prodigal | 0.996 | 0.989 | 0.995 / 0.971 | — | — | — | — | 0.970 | 0.900 | 0.729 / 0.417 | 0.321 | — | 0.935 |
| scoelicolor (validation blocks) | orf | 0.591 | 0.915 | 0.531 / 0.622 | — | — | — | — | 0.561 | 0.481 | 0.291 / 0.263 | 0.244 | — | 0.189 |
| mjannaschii (validation blocks) | genome_panel_ontmix_ft | 0.991 | 0.992 | 0.495 / 0.471 | 0.948 / 0.902 | 0.959 / 0.949 | 0.680 / 0.482 | 0.392 / 0.105 | 0.986 | 0.954 | 0.340 / 0.196 | 0.900 | 0.155 | 0.947 |
| mjannaschii (validation blocks) | prodigal | 0.994 | 0.994 | 0.990 / 0.980 | — | — | — | — | 0.933 | 0.767 | 0.546 / 0.257 | 0.529 | — | 0.926 |
| mjannaschii (validation blocks) | orf | 0.963 | 0.981 | 0.897 / 0.978 | — | — | — | — | 0.822 | 0.451 | 0.237 / 0.277 | 0.133 | — | 0.826 |
| bsubtilis (whole genome, held-out species) | genome_panel_ontmix_ft | 0.977 | 0.985 | 0.386 / 0.311 | 0.879 / 0.708 | 0.926 / 0.866 | 0.637 / 0.442 | 0.392 / 0.110 | 0.971 | 0.931 | 0.210 / 0.112 | 0.853 | 0.119 | 0.893 |
| bsubtilis (whole genome, held-out species) | prodigal | 0.993 | 0.992 | 0.975 / 0.977 | — | — | — | — | 0.956 | 0.825 | 0.545 / 0.313 | 0.502 | — | 0.874 |
| bsubtilis (whole genome, held-out species) | orf | 0.926 | 0.958 | 0.821 / 0.975 | — | — | — | — | 0.844 | 0.576 | 0.301 / 0.320 | 0.209 | — | 0.654 |
| spneumoniae (whole genome, held-out species) | genome_panel_ontmix_ft | 0.989 | 0.957 | 0.484 / 0.395 | 0.932 / 0.760 | 0.937 / 0.821 | 0.675 / 0.474 | 0.407 / 0.102 | 0.984 | 0.959 | 0.267 / 0.151 | 0.892 | 0.152 | 0.930 |
| spneumoniae (whole genome, held-out species) | prodigal | 0.983 | 0.967 | 0.962 / 0.887 | — | — | — | — | 0.948 | 0.823 | 0.558 / 0.282 | 0.559 | — | 0.904 |
| spneumoniae (whole genome, held-out species) | orf | 0.946 | 0.951 | 0.838 / 0.925 | — | — | — | — | 0.842 | 0.541 | 0.284 / 0.298 | 0.194 | — | 0.728 |
| dradiodurans (whole genome, held-out species) | genome_panel_ontmix_ft | 0.990 | 0.989 | 0.701 / 0.660 | 0.953 / 0.898 | 0.967 / 0.941 | 0.779 / 0.713 | 0.416 / 0.111 | 0.987 | 0.977 | 0.526 / 0.446 | 0.926 | 0.262 | 0.965 |
| dradiodurans (whole genome, held-out species) | prodigal | 0.991 | 0.990 | 0.989 / 0.987 | — | — | — | — | 0.971 | 0.907 | 0.714 / 0.434 | 0.525 | — | 0.928 |
| dradiodurans (whole genome, held-out species) | orf | 0.725 | 0.934 | 0.663 / 0.772 | — | — | — | — | 0.664 | 0.517 | 0.335 / 0.334 | 0.227 | — | 0.259 |
| tthermophilus (whole genome, held-out species) | genome_panel_ontmix_ft | 0.975 | 0.980 | 0.431 / 0.389 | 0.879 / 0.795 | 0.897 / 0.890 | 0.702 / 0.636 | 0.374 / 0.102 | 0.972 | 0.953 | 0.323 / 0.257 | 0.911 | 0.147 | 0.936 |
| tthermophilus (whole genome, held-out species) | prodigal | 0.995 | 0.989 | 0.989 / 0.973 | — | — | — | — | 0.973 | 0.899 | 0.706 / 0.399 | 0.532 | — | 0.933 |
| tthermophilus (whole genome, held-out species) | orf | 0.780 | 0.925 | 0.715 / 0.850 | — | — | — | — | 0.709 | 0.488 | 0.300 / 0.314 | 0.241 | — | 0.250 |
| hvolcanii (whole genome, held-out species) | genome_panel_ontmix_ft | 0.984 | 0.977 | 0.689 / 0.628 | 0.928 / 0.845 | 0.945 / 0.908 | 0.751 / 0.672 | 0.412 / 0.117 | 0.980 | 0.962 | 0.494 / 0.405 | 0.916 | 0.253 | 0.936 |
| hvolcanii (whole genome, held-out species) | prodigal | 0.991 | 0.984 | 0.987 / 0.962 | — | — | — | — | 0.956 | 0.852 | 0.662 / 0.416 | 0.374 | — | 0.927 |
| hvolcanii (whole genome, held-out species) | orf | 0.743 | 0.927 | 0.640 / 0.773 | — | — | — | — | 0.685 | 0.471 | 0.277 / 0.291 | 0.256 | — | 0.221 |
