# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | orf | 0.918 | 0.950 | 0.798 / 0.944 | — | 0.841 | 0.598 | 0.317 / 0.311 | 0.219 | — | 0.593 |
| ecoli (validation blocks) | prodigal | 0.991 | 0.978 | 0.953 / 0.945 | — | 0.966 | 0.846 | 0.592 / 0.329 | 0.528 | — | 0.902 |
| cjejuni (validation blocks) | orf | 0.944 | 0.960 | 0.886 / 0.951 | — | 0.849 | 0.543 | 0.273 / 0.258 | 0.175 | — | 0.774 |
| cjejuni (validation blocks) | prodigal | 0.998 | 0.983 | 1.000 / 0.917 | — | 0.960 | 0.797 | 0.602 / 0.265 | 0.567 | — | 0.947 |
| cdifficile (validation blocks) | orf | 0.955 | 0.974 | 0.905 / 0.975 | — | 0.845 | 0.495 | 0.269 / 0.299 | 0.151 | — | 0.766 |
| cdifficile (validation blocks) | prodigal | 0.998 | 0.995 | 0.994 / 0.980 | — | 0.945 | 0.779 | 0.512 / 0.247 | 0.522 | — | 0.918 |
| saureus (validation blocks) | orf | 0.953 | 0.971 | 0.857 / 0.984 | — | 0.839 | 0.496 | 0.263 / 0.307 | 0.135 | — | 0.769 |
| saureus (validation blocks) | prodigal | 0.992 | 0.991 | 0.956 / 0.982 | — | 0.944 | 0.783 | 0.495 / 0.253 | 0.521 | — | 0.931 |
| hpylori (validation blocks) | orf | 0.943 | 0.945 | 0.875 / 0.909 | — | 0.824 | 0.542 | 0.300 / 0.300 | 0.158 | — | 0.760 |
| hpylori (validation blocks) | prodigal | 0.993 | 0.962 | 0.988 / 0.888 | — | 0.964 | 0.854 | 0.662 / 0.283 | 0.579 | — | 0.899 |
| lmonocytogenes (validation blocks) | orf | 0.949 | 0.973 | 0.919 / 0.996 | — | 0.880 | 0.584 | 0.336 / 0.331 | 0.190 | — | 0.780 |
| lmonocytogenes (validation blocks) | prodigal | 0.999 | 0.998 | 1.000 / 0.990 | — | 0.965 | 0.836 | 0.597 / 0.318 | 0.548 | — | 0.921 |
| vcholerae (validation blocks) | orf | 0.950 | 0.975 | 0.896 / 0.982 | — | 0.876 | 0.642 | 0.369 / 0.306 | 0.192 | — | 0.734 |
| vcholerae (validation blocks) | prodigal | 0.997 | 0.996 | 0.988 / 0.976 | — | 0.968 | 0.869 | 0.618 / 0.302 | 0.561 | — | 0.920 |
| synechocystis (validation blocks) | orf | 0.939 | 0.965 | 0.824 / 0.981 | — | 0.828 | 0.549 | 0.333 / 0.336 | 0.172 | — | 0.687 |
| synechocystis (validation blocks) | prodigal | 0.994 | 0.991 | 0.984 / 0.958 | — | 0.963 | 0.868 | 0.663 / 0.313 | 0.553 | — | 0.878 |
| styphimurium (validation blocks) | orf | 0.938 | 0.972 | 0.858 / 0.972 | — | 0.864 | 0.610 | 0.368 / 0.330 | 0.218 | — | 0.538 |
| styphimurium (validation blocks) | prodigal | 0.992 | 0.992 | 0.978 / 0.965 | — | 0.957 | 0.853 | 0.630 / 0.335 | 0.528 | — | 0.887 |
| paeruginosa (validation blocks) | orf | 0.511 | 0.923 | 0.463 / 0.569 | — | 0.498 | 0.439 | 0.250 / 0.242 | 0.255 | — | 0.208 |
| paeruginosa (validation blocks) | prodigal | 0.996 | 0.993 | 0.998 / 0.969 | — | 0.975 | 0.907 | 0.719 / 0.414 | 0.474 | — | 0.950 |
| mtuberculosis (validation blocks) | orf | 0.820 | 0.933 | 0.726 / 0.794 | — | 0.776 | 0.575 | 0.334 / 0.290 | 0.242 | — | 0.403 |
| mtuberculosis (validation blocks) | prodigal | 0.983 | 0.981 | 0.986 / 0.943 | — | 0.954 | 0.877 | 0.660 / 0.370 | 0.482 | — | 0.863 |
| scoelicolor (validation blocks) | orf | 0.591 | 0.915 | 0.531 / 0.622 | — | 0.561 | 0.481 | 0.291 / 0.263 | 0.244 | — | 0.189 |
| scoelicolor (validation blocks) | prodigal | 0.996 | 0.989 | 0.995 / 0.971 | — | 0.970 | 0.900 | 0.729 / 0.417 | 0.321 | — | 0.935 |
| mjannaschii (validation blocks) | orf | 0.963 | 0.981 | 0.897 / 0.978 | — | 0.822 | 0.451 | 0.237 / 0.277 | 0.133 | — | 0.826 |
| mjannaschii (validation blocks) | prodigal | 0.994 | 0.994 | 0.990 / 0.980 | — | 0.933 | 0.767 | 0.546 / 0.257 | 0.529 | — | 0.926 |
| bsubtilis (whole genome, held-out species) | orf | 0.926 | 0.958 | 0.821 / 0.975 | — | 0.844 | 0.576 | 0.301 / 0.320 | 0.209 | — | 0.654 |
| bsubtilis (whole genome, held-out species) | prodigal | 0.993 | 0.992 | 0.975 / 0.977 | — | 0.956 | 0.825 | 0.545 / 0.313 | 0.502 | — | 0.874 |
| spneumoniae (whole genome, held-out species) | orf | 0.946 | 0.951 | 0.838 / 0.925 | — | 0.842 | 0.541 | 0.284 / 0.298 | 0.194 | — | 0.728 |
| spneumoniae (whole genome, held-out species) | prodigal | 0.983 | 0.967 | 0.962 / 0.887 | — | 0.948 | 0.823 | 0.558 / 0.282 | 0.559 | — | 0.904 |
| dradiodurans (whole genome, held-out species) | orf | 0.725 | 0.934 | 0.663 / 0.772 | — | 0.664 | 0.517 | 0.335 / 0.334 | 0.227 | — | 0.259 |
| dradiodurans (whole genome, held-out species) | prodigal | 0.991 | 0.990 | 0.989 / 0.987 | — | 0.971 | 0.907 | 0.714 / 0.434 | 0.525 | — | 0.928 |
| tthermophilus (whole genome, held-out species) | orf | 0.780 | 0.925 | 0.715 / 0.850 | — | 0.709 | 0.488 | 0.300 / 0.314 | 0.241 | — | 0.250 |
| tthermophilus (whole genome, held-out species) | prodigal | 0.995 | 0.989 | 0.989 / 0.973 | — | 0.973 | 0.899 | 0.706 / 0.399 | 0.532 | — | 0.933 |
| hvolcanii (whole genome, held-out species) | orf | 0.743 | 0.927 | 0.640 / 0.773 | — | 0.685 | 0.471 | 0.277 / 0.291 | 0.256 | — | 0.221 |
| hvolcanii (whole genome, held-out species) | prodigal | 0.991 | 0.984 | 0.987 / 0.962 | — | 0.956 | 0.852 | 0.662 / 0.416 | 0.374 | — | 0.927 |
