# GATACA — 2-bit organs

## Core idea
An **organ** reads a raw, unsegmented stream of 2-bit symbols (G/A/T/C = 00/01/10/11) and finds
the units in it by itself: nobody tells it where bytes, samples, characters or genes start. Organs
must be **robust**: they keep working when the stream starts at an arbitrary point, carries noise,
or comes in a different encoding.

The project has two tracks, each with its own document and its own Claude session:

| track | document | what it covers |
|---|---|---|
| **Tokenizers** | `TRACK_TOKENIZERS.md` | raw file bits: text (UTF-8 / cp1252), audio (PCM, mu-law), image (raw pixels) |
| **Genomics** | `TRACK_GENOMICS.md` | raw DNA: gene structure, reading frames, sequencing errors, real nanopore reads |

What each track learns feeds the other: the dilated conv stem that unblocked the genome organ also
took Spanish segmentation from F1 0.73 to 0.99.

## Robustness (every evaluation, one table)
- **Phase:** the stream starts at any symbol offset (mid-byte, mid-sample, mid-codon).
- **Noise:** random symbol substitutions; for DNA also insertions/deletions.
- **Encoding:** the same content in another encoding (UTF-8 vs cp1252; PCM16 vs PCM8 vs mu-law; ...).

## Shared infrastructure
- `gataca.py`: shared code (models `Organ`, `Segmenter`, `AudioOrgan`; noise, encodings, synthetic DNA,
  `Progress`, `update_metrics` with a lock file).
- `watch.py`: live progress console (bars for every run in `runs/progress/`, GPU, queue logs).
- `runs/<date>/metrics.json`: every result; `runs/*.log`: queue logs.
- `requirements.txt`; genomics also uses minimap2 in WSL (`tools/`).

## Rules
- Python/PyTorch for the experiment. C++ only once we know what needs speed.
- One script per step. Shared code goes in `gataca.py`.
- Log every run to `runs/<date>/metrics.json`. No experiment without a number.
- Every evaluation includes the robustness table. No robustness number, no claim.
- Every long job reports live progress (`gataca.Progress`, visible in `watch.py`).
- Code, comments and docs in English.

## References
- Byte Latent Transformer (Meta, 2024): dynamic byte patches from next-byte entropy.
- H-Net (2025): dynamic chunking learned end-to-end.
- ByT5, CANINE: tokenizer-free byte/character models.
- Bytes Are All You Need (Apple, 2023): classification from raw file bytes.
