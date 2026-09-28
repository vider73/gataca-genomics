# GATACA Genomics — reading genes straight from raw, error-laden DNA reads

A small neural network (~7M parameters) reads raw DNA, 2 bits per base, and labels every base with its
gene structure: non-coding, or coding on the forward/reverse strand at codon position 1, 2 or 3. It is
never told where genes or codons start. Because it knows the codon position of every base, it can
translate genes **through sequencing errors**, correcting frameshifts as it goes.

## The result: more real proteins from raw nanopore reads, with no reference database
Real Oxford Nanopore reads (2026 chemistry, 96.3% identity) of *Haloferax volcanii*, an archaeon the
model never saw in training. Each read is processed on its own, before any assembly. A gene counts as
recovered when one predicted protein matches it with >= 80% coverage and >= 80% identity.

| method (3,811 genes lying fully inside 299 reads) | genes recovered | precision |
|---|---|---|
| **this model (panel_aug + grammar decoder), 3 seeds** | **0.885 ± 0.003** | **0.903 ± 0.003** |
| FragGeneScanRs, best of 3 sequencing-error models | 0.864 | 0.833 – 0.850 |
| Prodigal, metagenomic mode | 0.257 | 0.699 |
| DIAMOND blastx, frameshift-aware (`--long-reads`), against the 13 training species | 0.259 | 0.948 |
| *DIAMOND against H. volcanii's own proteome (oracle: needs the answer's proteome)* | *0.963* | *0.974* |

- It beats FragGeneScan, the standard gene finder for error-prone reads, by **+2.1 points of recall and
  +5 points of precision**, consistently across seeds (every seed is above FragGeneScan's best model).
- It needs no reference proteins. Homology search without a close relative in the database finds
  about a quarter of the proteins; with the organism's own proteome (not available in practice for a
  new organism) it finds 96%.
- On the same reads it keeps the reading frame on 94.7% of coding bases, vs 57.7% for Prodigal.

Details: `runs/2026-09-28/proteins_report.md`, `runs/2026-09-28/seeds_report.md`.

## Honest limitations
- **The margin is small.** FragGeneScan is close (0.864 vs 0.885). This is an incremental improvement,
  not a new capability.
- **One species, one read set.** All real-read numbers come from one held-out archaeon. More species
  and simulated nanopore reads are needed before a general claim.
- **On clean genomes, Prodigal is better**: 0.991 vs 0.987 frame accuracy, and 0.980 vs 0.927 of genes
  with the exact stop codon. The model only pays off when the sequence has errors.
- **Prodigal on raw reads is a weak baseline** (it is not designed for them); FragGeneScan is the
  fair comparison.
- **Very noisy reads (2020 chemistry, 82% identity)**: no method recovers proteins at >= 80% identity.
  A nanopore-noise fine-tune (`panel_ontmix_ft`) reads 0.535 of the frame there (panel_aug 0.386,
  Prodigal 0.106), but that does not yet give usable proteins.
- Bacterial and archaeal genes only (no introns). Not yet compared with neural gene finders (e.g. Balrog).

## Robustness on 5 held-out species (mean, 3 seeds; synthetic errors on whole genomes)
| frame accuracy | Prodigal | panel_aug |
|---|---|---|
| clean genome | **0.991** | 0.987 |
| 5% substitutions | 0.861 | **0.970** |
| 1% insertions/deletions | 0.499 | **0.902** |
| 150 bp fragments | 0.913 | **0.942** |

Trained on 13 bacterial/archaeal species (GC 29–72%); held out: *B. subtilis*, *S. pneumoniae*,
*D. radiodurans*, *T. thermophilus*, *H. volcanii*.

## How it works
Model: `gataca.Segmenter(n_out=7, conv_layers=6)`: a 6-layer dilated convolution stem and 4 attention
blocks over 1,024-base windows, trained per base with noise augmentation (random substitutions and
indels; inserted bases carry no label, so the model learns to recover the original annotation across
frameshifts). A Viterbi decoder with a soft gene grammar (starts, stops, codons, frameshifts allowed at a
cost) turns per-base probabilities into genes. Proteins are translated with the model's own codon
positions: an inserted base is dropped, a missing one becomes X.

| step | script |
|---|---|
| download genomes from NCBI RefSeq, per-base labels (`--panel` for all 18) | `prepare_genome.py` |
| train (`--panel`, `--noise aug\|ont`, `--err-dist mix`, `--init`, `--seed`) | `train_genome.py` |
| robustness table vs Prodigal and a naive ORF rule | `eval_genome.py` |
| align real nanopore reads to the reference (minimap2), score frame accuracy | `prepare_nanopore.py`, `eval_nanopore.py` |
| proteins from raw reads vs FragGeneScanRs, DIAMOND, Prodigal | `compare_proteins.py` |
| grammar vs species-"accent" probe on synthetic genes | `probe_synthetic.py` |

```bash
pip install -r requirements.txt
python prepare_genome.py --panel
python train_genome.py --panel --noise aug --steps 12000 --run-name panel_aug
python eval_genome.py runs/<date>/genome_panel_aug.pt prodigal orf --panel
python compare_proteins.py runs/<date>/genome_panel_aug.pt prodigal fgs_454_10 diamond_panel --runs <nanopore run>
```
Training takes ~20 minutes on one RTX 4090. Every run logs to `runs/<date>/metrics.json`; `python watch.py`
shows live progress. The helper `detach.ps1` is specific to the author's
Windows machine; external tools (minimap2 in WSL, FragGeneScanRs, DIAMOND) go in `tools/`.

## Data and licences
Code: MIT (see `LICENSE`). Data is not in the repository; the scripts download and rebuild it.
- Genomes and annotations: NCBI RefSeq (assembly accessions in `data/genome_*/meta.json` once prepared).
- Nanopore reads: ENA/SRA runs ERR17000570 (2026 chemistry) and SRR11991309 (2020 chemistry).
- Tools used for comparison, not distributed: minimap2 (MIT), pyrodigal/Prodigal (GPL-3.0),
  FragGeneScanRs (GPL-3.0), DIAMOND (GPL-3.0).

## Context
Part of GATACA, an experiment on neural "organs" that find their own units in raw 2-bit streams
(see `GATACA.md`). A sister project applies the same idea to raw file bits (text, audio).
