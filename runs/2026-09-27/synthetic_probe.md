# Synthetic probe — gene mechanics vs E. coli accent

mechanics = ATG + random codons (no E. coli codon preference, no internal stop) + stop.
accent = E. coli codon usage with an in-frame stop every ~18 codons (not a gene).
An organ that learned the mechanics scores high in the ↑ columns and low in the ↓ ones.

| GC | target | mechanics: called coding ↑ | mechanics: frame acc ↑ | mechanics genes sens / prec ↑ | accent: called coding ↓ | filler: called coding ↓ |
|---|---|---|---|---|---|---|
| 35% | orf | 1.000 | 1.000 | 1.000 / 0.767 | 0.121 | 0.026 |
| 35% | prodigal | 1.000 | 0.997 | 1.000 / 0.361 | 0.355 | 0.184 |
| 35% | genome_g_conv_aug | 0.343 | 0.254 | 0.000 / 0.000 | 0.786 | 0.135 |
| 35% | genome_panel_aug | 0.335 | 0.294 | 0.000 / 0.000 | 0.647 | 0.072 |
| 35% | genome_panel_syn | 0.961 | 0.947 | 0.003 / 0.003 | 0.003 | 0.105 |
| 50% | orf | 0.998 | 0.993 | 0.987 / 0.700 | 0.136 | 0.087 |
| 50% | prodigal | 0.999 | 0.991 | 0.990 / 0.318 | 0.391 | 0.293 |
| 50% | genome_g_conv_aug | 0.223 | 0.078 | 0.003 / 0.001 | 0.781 | 0.287 |
| 50% | genome_panel_aug | 0.130 | 0.073 | 0.007 / 0.003 | 0.653 | 0.154 |
| 50% | genome_panel_syn | 0.886 | 0.845 | 0.003 / 0.002 | 0.023 | 0.202 |
| 65% | orf | 0.987 | 0.956 | 0.920 / 0.596 | 0.158 | 0.212 |
| 65% | prodigal | 0.945 | 0.841 | 0.797 / 0.343 | 0.259 | 0.385 |
| 65% | genome_g_conv_aug | 0.099 | 0.026 | 0.000 / 0.000 | 0.689 | 0.193 |
| 65% | genome_panel_aug | 0.011 | 0.003 | 0.000 / 0.000 | 0.539 | 0.060 |
| 65% | genome_panel_syn | 0.864 | 0.679 | 0.000 / 0.000 | 0.005 | 0.156 |
