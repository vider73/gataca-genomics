# GATACA — Genomics track

**Status: STAND BY since 2026-09-29**, until the sister project (tokenizers, `I:\LLMLab\GaTaCa`) is in shape.
No jobs running or queued. Repo: `github.com/vider73/gataca-genomics` (public, MIT). Folder:
`I:\LLMLab\GaTaCa-Genomics`.

## What it is
An organ (`gataca.Segmenter(n_out=7, conv_layers=6)`, ~7M params) reads raw DNA, 2 bits per base, and
labels each base: non-coding, or forward/reverse strand at codon position 1-3. Trained on 13
bacterial/archaeal species (`data/panel.json`), tested on 5 held-out species and real nanopore reads of
*H. volcanii* (held-out archaeon). A Viterbi grammar decoder turns labels into genes; proteins are
translated with the organ's own codon positions, so frameshifts are corrected.

## Where it stands (3 seeds each; reports in `runs/2026-09-28/`)
- **Proteins from raw 2026 nanopore reads** (`proteins_report.md`, `seeds_report.md`): organ `panel_aug`
  0.885 ± 0.003 of genes recovered, precision 0.903, vs FragGeneScanRs 0.864 / 0.85, Prodigal 0.26,
  DIAMOND -F without a close reference 0.26, DIAMOND with the organism's own proteome (oracle) 0.96.
  Best non-oracle method, by a small margin.
- **Robustness, 5 held-out species**: frame accuracy clean 0.987 (Prodigal 0.991), 5% subs 0.970 (0.861),
  1% indels 0.902 (0.499), 150 bp fragments 0.942 (0.913). Prodigal is better on clean genomes.
- **Very noisy reads (2020, 82% identity)**: nobody recovers proteins. A nanopore-noise fine-tune
  (`panel_ontmix_ft`: `--noise ont --err-dist mix`, from panel_aug) reads 0.535 of the frame (panel_aug 0.386).
- Lessons: the noise *rate distribution* mattered more than the error model; an error-aware decoder cost
  did not help; organs trained on real genomes learn species "accent", not gene grammar (`synthetic_probe.md`).

## Checkpoints (local, not in git)
`runs/2026-09-26/genome_panel_aug.pt` (default), seeds `runs/2026-09-28/genome_panel_aug_s{1,2}.pt`;
`runs/2026-09-27/genome_panel_ontmix_ft.pt` (very noisy reads); `runs/2026-09-28/genome_panel_ontmix_sub_ft.pt`.

## To resume
- Scripts: `prepare_genome.py`, `train_genome.py`, `eval_genome.py`, `prepare_nanopore.py`,
  `eval_nanopore.py`, `compare_proteins.py`, `probe_synthetic.py` (usage in `README.md`).
- GPU: every GPU command through `python I:/LLMLab/GPUControl/gpu.py run --project genomics --name <job> --
  "<absolute python.exe>" <script> ...` (a bare `python` resolves to an interpreter without numpy); long jobs
  detached with `detach.ps1`. Tools in `tools/`: minimap2 and FragGeneScanRs (WSL), DIAMOND (Windows).

## Next, when resumed
1. The protein gain on more species: simulated nanopore reads of the 4 other held-out genomes, and a
   metagenome-like mix with rare species.
2. A neural gene finder (Balrog) in the protein comparison.
3. A grammar probe independent of the synthetic generator.
4. Later: learned units on DNA (the tokenizer idea applied to genomes); eukaryotes with introns.
