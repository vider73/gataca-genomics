# Genomics G1 — gene structure from raw bases

Frame acc: annotated coding bases with the right strand and codon position. Genes: exact stop-codon match.
Prodigal trains itself on each genome it is given (including noisy ones); on fragments it runs in meta mode.

| genome | target | frame acc | coding F1 | genes sens / prec | genes + stop snap | frame acc sub 1% | frame acc sub 5% | genes sens / prec sub 5% | frame acc indel 1% | gene sens indel 1% | frame acc 150 bp fragments |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ecoli (validation blocks) | orf | 0.918 | 0.950 | 0.798 / 0.944 | — | 0.841 | 0.598 | 0.317 / 0.311 | 0.219 | — | 0.593 |
| ecoli (validation blocks) | prodigal | 0.991 | 0.978 | 0.953 / 0.945 | — | 0.966 | 0.846 | 0.592 / 0.329 | 0.528 | — | 0.902 |
| ecoli (validation blocks) | genome_g_conv_aug | 0.975 | 0.970 | 0.312 / 0.288 | 0.874 / 0.809 | 0.973 | 0.957 | 0.228 / 0.178 | 0.891 | 0.120 | 0.930 |
| ecoli (validation blocks) | genome_panel_aug | 0.983 | 0.974 | 0.529 / 0.513 | 0.903 / 0.876 | 0.981 | 0.966 | 0.338 / 0.285 | 0.893 | 0.191 | 0.944 |
| ecoli (validation blocks) | genome_panel_syn | 0.981 | 0.973 | 0.298 / 0.284 | 0.895 / 0.851 | 0.979 | 0.960 | 0.215 / 0.173 | 0.888 | 0.118 | 0.923 |
| cjejuni (validation blocks) | orf | 0.944 | 0.960 | 0.886 / 0.951 | — | 0.849 | 0.543 | 0.273 / 0.258 | 0.175 | — | 0.774 |
| cjejuni (validation blocks) | prodigal | 0.998 | 0.983 | 1.000 / 0.917 | — | 0.960 | 0.797 | 0.602 / 0.265 | 0.567 | — | 0.947 |
| cjejuni (validation blocks) | genome_g_conv_aug | 0.989 | 0.972 | 0.091 / 0.083 | 0.818 / 0.750 | 0.986 | 0.972 | 0.068 / 0.044 | 0.874 | 0.034 | 0.923 |
| cjejuni (validation blocks) | genome_panel_aug | 0.995 | 0.976 | 0.352 / 0.330 | 0.920 / 0.862 | 0.994 | 0.987 | 0.250 / 0.193 | 0.919 | 0.045 | 0.978 |
| cjejuni (validation blocks) | genome_panel_syn | 0.995 | 0.975 | 0.261 / 0.253 | 0.886 / 0.857 | 0.994 | 0.985 | 0.170 / 0.125 | 0.912 | 0.023 | 0.976 |
| cdifficile (validation blocks) | orf | 0.955 | 0.974 | 0.905 / 0.975 | — | 0.845 | 0.495 | 0.269 / 0.299 | 0.151 | — | 0.766 |
| cdifficile (validation blocks) | prodigal | 0.998 | 0.995 | 0.994 / 0.980 | — | 0.945 | 0.779 | 0.512 / 0.247 | 0.522 | — | 0.918 |
| cdifficile (validation blocks) | genome_g_conv_aug | 0.981 | 0.969 | 0.130 / 0.112 | 0.766 / 0.659 | 0.979 | 0.958 | 0.064 / 0.044 | 0.848 | 0.052 | 0.827 |
| cdifficile (validation blocks) | genome_panel_aug | 0.995 | 0.988 | 0.491 / 0.461 | 0.960 / 0.900 | 0.994 | 0.981 | 0.353 / 0.290 | 0.916 | 0.185 | 0.970 |
| cdifficile (validation blocks) | genome_panel_syn | 0.994 | 0.986 | 0.292 / 0.276 | 0.954 / 0.902 | 0.992 | 0.974 | 0.220 / 0.172 | 0.911 | 0.090 | 0.961 |
| saureus (validation blocks) | orf | 0.953 | 0.971 | 0.857 / 0.984 | — | 0.839 | 0.496 | 0.263 / 0.307 | 0.135 | — | 0.769 |
| saureus (validation blocks) | prodigal | 0.992 | 0.991 | 0.956 / 0.982 | — | 0.944 | 0.783 | 0.495 / 0.253 | 0.521 | — | 0.931 |
| saureus (validation blocks) | genome_g_conv_aug | 0.986 | 0.978 | 0.160 / 0.159 | 0.833 / 0.824 | 0.984 | 0.967 | 0.102 / 0.086 | 0.877 | 0.068 | 0.922 |
| saureus (validation blocks) | genome_panel_aug | 0.990 | 0.988 | 0.553 / 0.572 | 0.925 / 0.958 | 0.988 | 0.979 | 0.345 / 0.303 | 0.916 | 0.171 | 0.973 |
| saureus (validation blocks) | genome_panel_syn | 0.992 | 0.988 | 0.304 / 0.310 | 0.932 / 0.951 | 0.989 | 0.966 | 0.188 / 0.162 | 0.911 | 0.082 | 0.967 |
| hpylori (validation blocks) | orf | 0.943 | 0.945 | 0.875 / 0.909 | — | 0.824 | 0.542 | 0.300 / 0.300 | 0.158 | — | 0.760 |
| hpylori (validation blocks) | prodigal | 0.993 | 0.962 | 0.988 / 0.888 | — | 0.964 | 0.854 | 0.662 / 0.283 | 0.579 | — | 0.899 |
| hpylori (validation blocks) | genome_g_conv_aug | 0.944 | 0.937 | 0.087 / 0.051 | 0.688 / 0.399 | 0.925 | 0.857 | 0.075 / 0.037 | 0.761 | 0.000 | 0.758 |
| hpylori (validation blocks) | genome_panel_aug | 0.987 | 0.950 | 0.312 / 0.263 | 0.863 / 0.726 | 0.986 | 0.976 | 0.237 / 0.168 | 0.896 | 0.138 | 0.934 |
| hpylori (validation blocks) | genome_panel_syn | 0.987 | 0.949 | 0.212 / 0.185 | 0.838 / 0.728 | 0.987 | 0.970 | 0.138 / 0.092 | 0.891 | 0.100 | 0.933 |
| lmonocytogenes (validation blocks) | orf | 0.949 | 0.973 | 0.919 / 0.996 | — | 0.880 | 0.584 | 0.336 / 0.331 | 0.190 | — | 0.780 |
| lmonocytogenes (validation blocks) | prodigal | 0.999 | 0.998 | 1.000 / 0.990 | — | 0.965 | 0.836 | 0.597 / 0.318 | 0.548 | — | 0.921 |
| lmonocytogenes (validation blocks) | genome_g_conv_aug | 0.983 | 0.988 | 0.176 / 0.148 | 0.868 / 0.729 | 0.978 | 0.960 | 0.112 / 0.075 | 0.859 | 0.064 | 0.904 |
| lmonocytogenes (validation blocks) | genome_panel_aug | 0.996 | 0.996 | 0.536 / 0.525 | 0.969 / 0.950 | 0.994 | 0.984 | 0.407 / 0.331 | 0.908 | 0.169 | 0.969 |
| lmonocytogenes (validation blocks) | genome_panel_syn | 0.994 | 0.995 | 0.302 / 0.292 | 0.969 / 0.938 | 0.992 | 0.980 | 0.193 / 0.149 | 0.902 | 0.088 | 0.962 |
| vcholerae (validation blocks) | orf | 0.950 | 0.975 | 0.896 / 0.982 | — | 0.876 | 0.642 | 0.369 / 0.306 | 0.192 | — | 0.734 |
| vcholerae (validation blocks) | prodigal | 0.997 | 0.996 | 0.988 / 0.976 | — | 0.968 | 0.869 | 0.618 / 0.302 | 0.561 | — | 0.920 |
| vcholerae (validation blocks) | genome_g_conv_aug | 0.987 | 0.990 | 0.337 / 0.277 | 0.888 / 0.729 | 0.985 | 0.969 | 0.205 / 0.127 | 0.889 | 0.104 | 0.937 |
| vcholerae (validation blocks) | genome_panel_aug | 0.991 | 0.994 | 0.598 / 0.587 | 0.932 / 0.913 | 0.989 | 0.979 | 0.450 / 0.365 | 0.905 | 0.201 | 0.963 |
| vcholerae (validation blocks) | genome_panel_syn | 0.989 | 0.992 | 0.365 / 0.360 | 0.912 / 0.897 | 0.987 | 0.973 | 0.257 / 0.195 | 0.898 | 0.112 | 0.954 |
| synechocystis (validation blocks) | orf | 0.939 | 0.965 | 0.824 / 0.981 | — | 0.828 | 0.549 | 0.333 / 0.336 | 0.172 | — | 0.687 |
| synechocystis (validation blocks) | prodigal | 0.994 | 0.991 | 0.984 / 0.958 | — | 0.963 | 0.868 | 0.663 / 0.313 | 0.553 | — | 0.878 |
| synechocystis (validation blocks) | genome_g_conv_aug | 0.915 | 0.947 | 0.149 / 0.095 | 0.667 / 0.425 | 0.905 | 0.846 | 0.094 / 0.048 | 0.754 | 0.039 | 0.786 |
| synechocystis (validation blocks) | genome_panel_aug | 0.985 | 0.980 | 0.529 / 0.500 | 0.898 / 0.848 | 0.983 | 0.971 | 0.361 / 0.272 | 0.891 | 0.192 | 0.942 |
| synechocystis (validation blocks) | genome_panel_syn | 0.986 | 0.978 | 0.325 / 0.311 | 0.902 / 0.861 | 0.984 | 0.968 | 0.212 / 0.148 | 0.883 | 0.106 | 0.929 |
| styphimurium (validation blocks) | orf | 0.938 | 0.972 | 0.858 / 0.972 | — | 0.864 | 0.610 | 0.368 / 0.330 | 0.218 | — | 0.538 |
| styphimurium (validation blocks) | prodigal | 0.992 | 0.992 | 0.978 / 0.965 | — | 0.957 | 0.853 | 0.630 / 0.335 | 0.528 | — | 0.887 |
| styphimurium (validation blocks) | genome_g_conv_aug | 0.977 | 0.983 | 0.302 / 0.265 | 0.882 / 0.774 | 0.974 | 0.956 | 0.208 / 0.148 | 0.885 | 0.100 | 0.935 |
| styphimurium (validation blocks) | genome_panel_aug | 0.986 | 0.988 | 0.548 / 0.516 | 0.929 / 0.875 | 0.983 | 0.970 | 0.375 / 0.311 | 0.892 | 0.153 | 0.947 |
| styphimurium (validation blocks) | genome_panel_syn | 0.984 | 0.987 | 0.306 / 0.283 | 0.911 / 0.842 | 0.981 | 0.962 | 0.231 / 0.183 | 0.882 | 0.078 | 0.932 |
| paeruginosa (validation blocks) | orf | 0.511 | 0.923 | 0.463 / 0.569 | — | 0.498 | 0.439 | 0.250 / 0.242 | 0.255 | — | 0.208 |
| paeruginosa (validation blocks) | prodigal | 0.996 | 0.993 | 0.998 / 0.969 | — | 0.975 | 0.907 | 0.719 / 0.414 | 0.474 | — | 0.950 |
| paeruginosa (validation blocks) | genome_g_conv_aug | 0.977 | 0.960 | 0.150 / 0.129 | 0.864 / 0.743 | 0.974 | 0.955 | 0.095 / 0.071 | 0.915 | 0.029 | 0.919 |
| paeruginosa (validation blocks) | genome_panel_aug | 0.994 | 0.989 | 0.785 / 0.735 | 0.980 / 0.918 | 0.994 | 0.991 | 0.626 / 0.580 | 0.950 | 0.288 | 0.981 |
| paeruginosa (validation blocks) | genome_panel_syn | 0.993 | 0.988 | 0.635 / 0.603 | 0.964 / 0.915 | 0.993 | 0.988 | 0.521 / 0.477 | 0.946 | 0.216 | 0.976 |
| mtuberculosis (validation blocks) | orf | 0.820 | 0.933 | 0.726 / 0.794 | — | 0.776 | 0.575 | 0.334 / 0.290 | 0.242 | — | 0.403 |
| mtuberculosis (validation blocks) | prodigal | 0.983 | 0.981 | 0.986 / 0.943 | — | 0.954 | 0.877 | 0.660 / 0.370 | 0.482 | — | 0.863 |
| mtuberculosis (validation blocks) | genome_g_conv_aug | 0.846 | 0.924 | 0.031 / 0.015 | 0.637 / 0.311 | 0.840 | 0.794 | 0.037 / 0.016 | 0.731 | 0.011 | 0.739 |
| mtuberculosis (validation blocks) | genome_panel_aug | 0.970 | 0.977 | 0.409 / 0.345 | 0.891 / 0.754 | 0.968 | 0.954 | 0.306 / 0.235 | 0.877 | 0.143 | 0.907 |
| mtuberculosis (validation blocks) | genome_panel_syn | 0.966 | 0.970 | 0.249 / 0.206 | 0.854 / 0.707 | 0.963 | 0.946 | 0.206 / 0.153 | 0.868 | 0.097 | 0.883 |
| scoelicolor (validation blocks) | orf | 0.591 | 0.915 | 0.531 / 0.622 | — | 0.561 | 0.481 | 0.291 / 0.263 | 0.244 | — | 0.189 |
| scoelicolor (validation blocks) | prodigal | 0.996 | 0.989 | 0.995 / 0.971 | — | 0.970 | 0.900 | 0.729 / 0.417 | 0.321 | — | 0.935 |
| scoelicolor (validation blocks) | genome_g_conv_aug | 0.824 | 0.910 | 0.050 / 0.032 | 0.572 / 0.365 | 0.815 | 0.773 | 0.029 / 0.015 | 0.723 | 0.014 | 0.699 |
| scoelicolor (validation blocks) | genome_panel_aug | 0.991 | 0.985 | 0.697 / 0.634 | 0.952 / 0.866 | 0.990 | 0.985 | 0.548 / 0.470 | 0.939 | 0.243 | 0.965 |
| scoelicolor (validation blocks) | genome_panel_syn | 0.990 | 0.983 | 0.591 / 0.533 | 0.950 / 0.857 | 0.989 | 0.982 | 0.434 / 0.359 | 0.934 | 0.192 | 0.957 |
| mjannaschii (validation blocks) | orf | 0.963 | 0.981 | 0.897 / 0.978 | — | 0.822 | 0.451 | 0.237 / 0.277 | 0.133 | — | 0.826 |
| mjannaschii (validation blocks) | prodigal | 0.994 | 0.994 | 0.990 / 0.980 | — | 0.933 | 0.767 | 0.546 / 0.257 | 0.529 | — | 0.926 |
| mjannaschii (validation blocks) | genome_g_conv_aug | 0.946 | 0.971 | 0.093 / 0.065 | 0.753 / 0.529 | 0.930 | 0.875 | 0.093 / 0.054 | 0.745 | 0.031 | 0.733 |
| mjannaschii (validation blocks) | genome_panel_aug | 0.992 | 0.993 | 0.454 / 0.431 | 0.948 / 0.902 | 0.988 | 0.968 | 0.392 / 0.277 | 0.897 | 0.175 | 0.957 |
| mjannaschii (validation blocks) | genome_panel_syn | 0.991 | 0.991 | 0.289 / 0.277 | 0.959 / 0.921 | 0.987 | 0.959 | 0.196 / 0.135 | 0.889 | 0.082 | 0.952 |
| bsubtilis (whole genome, held-out species) | orf | 0.926 | 0.958 | 0.821 / 0.975 | — | 0.844 | 0.576 | 0.301 / 0.320 | 0.209 | — | 0.654 |
| bsubtilis (whole genome, held-out species) | prodigal | 0.993 | 0.992 | 0.975 / 0.977 | — | 0.956 | 0.825 | 0.545 / 0.313 | 0.502 | — | 0.874 |
| bsubtilis (whole genome, held-out species) | genome_g_conv_aug | 0.950 | 0.973 | 0.127 / 0.084 | 0.735 / 0.489 | 0.943 | 0.897 | 0.076 / 0.041 | 0.804 | 0.046 | 0.825 |
| bsubtilis (whole genome, held-out species) | genome_panel_aug | 0.983 | 0.986 | 0.420 / 0.379 | 0.902 / 0.815 | 0.979 | 0.954 | 0.262 / 0.184 | 0.858 | 0.139 | 0.915 |
| bsubtilis (whole genome, held-out species) | genome_panel_syn | 0.980 | 0.985 | 0.237 / 0.208 | 0.873 / 0.768 | 0.975 | 0.943 | 0.148 / 0.095 | 0.846 | 0.078 | 0.895 |
| spneumoniae (whole genome, held-out species) | orf | 0.946 | 0.951 | 0.838 / 0.925 | — | 0.842 | 0.541 | 0.284 / 0.298 | 0.194 | — | 0.728 |
| spneumoniae (whole genome, held-out species) | prodigal | 0.983 | 0.967 | 0.962 / 0.887 | — | 0.948 | 0.823 | 0.558 / 0.282 | 0.559 | — | 0.904 |
| spneumoniae (whole genome, held-out species) | genome_g_conv_aug | 0.962 | 0.948 | 0.146 / 0.104 | 0.773 / 0.550 | 0.954 | 0.916 | 0.092 / 0.054 | 0.824 | 0.042 | 0.830 |
| spneumoniae (whole genome, held-out species) | genome_panel_aug | 0.990 | 0.957 | 0.492 / 0.426 | 0.928 / 0.804 | 0.987 | 0.972 | 0.312 / 0.227 | 0.891 | 0.168 | 0.939 |
| spneumoniae (whole genome, held-out species) | genome_panel_syn | 0.984 | 0.955 | 0.299 / 0.261 | 0.910 / 0.794 | 0.979 | 0.959 | 0.193 / 0.137 | 0.878 | 0.103 | 0.930 |
| dradiodurans (whole genome, held-out species) | orf | 0.725 | 0.934 | 0.663 / 0.772 | — | 0.664 | 0.517 | 0.335 / 0.334 | 0.227 | — | 0.259 |
| dradiodurans (whole genome, held-out species) | prodigal | 0.991 | 0.990 | 0.989 / 0.987 | — | 0.971 | 0.907 | 0.714 / 0.434 | 0.525 | — | 0.928 |
| dradiodurans (whole genome, held-out species) | genome_g_conv_aug | 0.950 | 0.963 | 0.181 / 0.149 | 0.792 / 0.652 | 0.945 | 0.921 | 0.130 / 0.093 | 0.864 | 0.064 | 0.872 |
| dradiodurans (whole genome, held-out species) | genome_panel_aug | 0.991 | 0.989 | 0.714 / 0.684 | 0.956 / 0.916 | 0.989 | 0.983 | 0.551 / 0.511 | 0.928 | 0.273 | 0.968 |
| dradiodurans (whole genome, held-out species) | genome_panel_syn | 0.988 | 0.988 | 0.564 / 0.538 | 0.949 / 0.904 | 0.987 | 0.979 | 0.430 / 0.391 | 0.921 | 0.216 | 0.953 |
| tthermophilus (whole genome, held-out species) | orf | 0.780 | 0.925 | 0.715 / 0.850 | — | 0.709 | 0.488 | 0.300 / 0.314 | 0.241 | — | 0.250 |
| tthermophilus (whole genome, held-out species) | prodigal | 0.995 | 0.989 | 0.989 / 0.973 | — | 0.973 | 0.899 | 0.706 / 0.399 | 0.532 | — | 0.933 |
| tthermophilus (whole genome, held-out species) | genome_g_conv_aug | 0.185 | 0.334 | 0.010 / 0.033 | 0.069 / 0.214 | 0.182 | 0.160 | 0.005 / 0.015 | 0.101 | 0.002 | 0.327 |
| tthermophilus (whole genome, held-out species) | genome_panel_aug | 0.983 | 0.983 | 0.430 / 0.414 | 0.892 / 0.858 | 0.982 | 0.971 | 0.345 / 0.318 | 0.916 | 0.159 | 0.949 |
| tthermophilus (whole genome, held-out species) | genome_panel_syn | 0.978 | 0.980 | 0.300 / 0.290 | 0.861 / 0.830 | 0.977 | 0.963 | 0.243 / 0.216 | 0.903 | 0.115 | 0.915 |
| hvolcanii (whole genome, held-out species) | orf | 0.743 | 0.927 | 0.640 / 0.773 | — | 0.685 | 0.471 | 0.277 / 0.291 | 0.256 | — | 0.221 |
| hvolcanii (whole genome, held-out species) | prodigal | 0.991 | 0.984 | 0.987 / 0.962 | — | 0.956 | 0.852 | 0.662 / 0.416 | 0.374 | — | 0.927 |
| hvolcanii (whole genome, held-out species) | genome_g_conv_aug | 0.823 | 0.908 | 0.074 / 0.051 | 0.565 / 0.391 | 0.813 | 0.773 | 0.046 / 0.029 | 0.728 | 0.025 | 0.741 |
| hvolcanii (whole genome, held-out species) | genome_panel_aug | 0.987 | 0.978 | 0.697 / 0.652 | 0.933 / 0.872 | 0.984 | 0.973 | 0.530 / 0.469 | 0.920 | 0.264 | 0.944 |
| hvolcanii (whole genome, held-out species) | genome_panel_syn | 0.985 | 0.975 | 0.570 / 0.522 | 0.921 / 0.845 | 0.982 | 0.965 | 0.417 / 0.364 | 0.913 | 0.217 | 0.927 |
