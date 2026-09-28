# Synthetic probe — gene mechanics vs E. coli accent

mechanics = ATG + random codons (no E. coli codon preference, no internal stop) + stop.
accent = E. coli codon usage with an in-frame stop every ~18 codons (not a gene).
An organ that learned the mechanics scores high in the ↑ columns and low in the ↓ ones.

| GC | target | mechanics: called coding ↑ | mechanics: frame acc ↑ | mechanics genes sens / prec ↑ | accent: called coding ↓ | filler: called coding ↓ |
|---|---|---|---|---|---|---|
| 35% | orf | 1.000 | 1.000 | 1.000 / 0.767 | 0.121 | 0.026 |
| 35% | prodigal | 1.000 | 0.997 | 1.000 / 0.361 | 0.355 | 0.184 |
| 35% | genome_g_conv_none | 0.258 | 0.254 | 0.003 / 0.005 | 0.138 | 0.027 |
| 35% | genome_g_conv_aug | 0.343 | 0.254 | 0.000 / 0.000 | 0.786 | 0.135 |
| 50% | orf | 0.998 | 0.993 | 0.987 / 0.700 | 0.136 | 0.087 |
| 50% | prodigal | 0.999 | 0.991 | 0.990 / 0.318 | 0.391 | 0.293 |
| 50% | genome_g_conv_none | 0.059 | 0.051 | 0.000 / 0.000 | 0.122 | 0.021 |
| 50% | genome_g_conv_aug | 0.223 | 0.078 | 0.003 / 0.001 | 0.781 | 0.287 |
| 65% | orf | 0.987 | 0.956 | 0.920 / 0.596 | 0.158 | 0.212 |
| 65% | prodigal | 0.945 | 0.841 | 0.797 / 0.343 | 0.259 | 0.385 |
| 65% | genome_g_conv_none | 0.007 | 0.005 | 0.000 / 0.000 | 0.128 | 0.015 |
| 65% | genome_g_conv_aug | 0.099 | 0.026 | 0.000 / 0.000 | 0.689 | 0.193 |
