# GATACA Genomics — gene structure read from raw, error-laden DNA

A small neural "organ" reads raw DNA (natively 2-bit: G/A/T/C = 00/01/10/11) and labels every base
with its gene structure: non-coding, or coding on the forward/reverse strand at codon position 1, 2
or 3. Nobody tells it where genes or codons start. The goal is **robustness**: reads that start
anywhere, sequencing errors (substitutions and, above all, insertions/deletions that shift the
reading frame), short fragments and species it has never seen.

Codons play the role of bytes and the reading frame plays the role of byte alignment. The same idea
applied to raw file bits (text, audio) lives in a sister project, *GATACA tokenizers*, which shares
the model code (`gataca.py`) but not the data or results.

## Main results (details and caveats in `runs/*/*.md` and `TRACK_GENOMICS.md`)
Organ: `gataca.Segmenter(n_out=7, conv_layers=6)`, ~7M parameters (dilated conv stem + 4 attention
blocks), trained on 13 bacterial/archaeal species; evaluated on 5 held-out species.

| mean over 5 held-out species | Prodigal | organ `panel_aug` | organ `panel_ontmix_ft` |
|---|---|---|---|
| frame accuracy, clean genome | **0.991** | 0.987 | 0.983 |
| frame accuracy, 5% substitutions | 0.861 | **0.971** | 0.956 |
| frame accuracy, 1% indels | 0.499 | **0.902** | 0.900 |
| frame accuracy, 150 bp fragments | 0.913 | **0.943** | 0.932 |

Real nanopore reads of *Haloferax volcanii* (an archaeon never seen in training), each read on its own:

| frame accuracy | 2026 reads (96.3% identity) | same stretches, no errors | 2020 reads (82.2% identity) |
|---|---|---|---|
| Prodigal (meta mode) | 0.577 | **0.994** | 0.106 |
| organ `panel_aug` | **0.947** | 0.989 | 0.386 |
| organ `panel_ontmix_ft` | 0.945 | 0.988 | **0.542** |

Caveats:
- Prodigal is better on clean genomes and at exact gene boundaries (genes with the exact stop codon,
  clean: 0.980 vs 0.930 for the organ + grammar decoder). The organ's advantage is under errors.
- Gene-level precision on reads is not yet fair: genes cut by a read's end count as false predictions.
- One held-out species for real reads, one seed per organ: no error bars yet.
- Tools built for error-prone reads (FragGeneScan) and neural gene finders (Balrog) are not compared yet.
- The synthetic "grammar" probe uses the same generator as the synthetic training data.

## How it works
| step | script |
|---|---|
| download genomes from NCBI RefSeq, per-base labels (`--panel` for all 18) | `prepare_genome.py` |
| train an organ (`--panel`, `--noise aug\|ont`, `--err-dist mix`, `--init`) | `train_genome.py` |
| robustness table vs Prodigal and a naive ORF rule (`--panel`) | `eval_genome.py` |
| grammar vs "accent" probe on synthetic genes | `probe_synthetic.py` |
| align real nanopore reads (minimap2 in WSL), then score on them | `prepare_nanopore.py`, `eval_nanopore.py` |

Training noise: `--noise aug` (uniform substitutions + indels) or `--noise ont` (`gataca.mutate_nanopore`:
indel-heavy, homopolymer-biased, bursty; a published nanopore error profile, not fit to the test reads).
Genes are read off the per-base labels with a Viterbi grammar decoder (`eval_genome.grammar_decode`).

```bash
pip install -r requirements.txt
python prepare_genome.py --panel
python train_genome.py --panel --noise aug --steps 12000 --run-name panel_aug
python train_genome.py --panel --noise ont --err-dist mix --err-max 0.25 --init runs/<date>/genome_panel_aug.pt --steps 4000 --lr 2e-4 --warmup 100 --run-name panel_ontmix_ft
python eval_genome.py runs/<date>/genome_panel_ontmix_ft.pt prodigal orf --panel
```

Every run logs to `runs/<date>/metrics.json` and reports live progress to `runs/progress/`; watch with
`python watch.py`. Long jobs run detached with `detach.ps1` (Windows scheduled task). The GPU is shared
with the sister project: one job at a time, queued behind `gpu_idle.py`.

## Data and licences
Not in the repository (see `.gitignore`); scripts download and rebuild it.
- Genomes and annotations: NCBI RefSeq (public domain in the US; NCBI asks for citation of the
  original submitters). Training: E. coli K-12 MG1655, C. jejuni, C. difficile, S. aureus, H. pylori,
  L. monocytogenes, V. cholerae, Synechocystis, S. Typhimurium, P. aeruginosa, M. tuberculosis,
  S. coelicolor, M. jannaschii. Held-out: B. subtilis, S. pneumoniae, D. radiodurans, T. thermophilus,
  H. volcanii. Assembly accessions in `data/genome_*/meta.json`.
- Nanopore reads: ENA/SRA runs ERR17000570 (2026 chemistry) and SRR11991309 (2020), public archive data.
- Tools: minimap2 (MIT), Prodigal via pyrodigal (GPL-3.0; used as a baseline, not distributed here).
