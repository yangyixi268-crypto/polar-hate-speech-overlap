# Polarization–Hate Speech Overlap

Course project for *Hate Speech Detection* (LMU München, WiSe 2026/27).

> **Content warning:** This project deals with offensive and hateful language.

## Project Overview

Polarization and hate speech are related but distinct phenomena.
This project annotates a subset of English POLAR data for hate speech
and analyzes where the two phenomena converge and diverge.

**Research questions**
1. To what extent do polarization and hate speech overlap in English POLAR data?
2. Which polarization types and manifestations are most strongly associated with hate speech?
3. What characterizes the instances in which the two labels disagree?

## Data

This project uses the English portion of
[POLAR](https://github.com/Polar-SemEval/data-public) (SemEval-2026 Task 9),
licensed under CC BY 4.0.

**The data is not included in this repository.** POLAR contains a canary
string and should not appear in web-crawled training corpora. To reproduce
the results, clone the official repository into the project root:

    git clone https://github.com/Polar-SemEval/data-public.git

**Sample:** 300 instances from the English test split
(150 polarized, 150 non-polarized, random seed 42).
`data/sample_ids.csv` lists their IDs.

## Repository Structure

| Folder | Content |
|---|---|
| `notebooks/` | Data exploration, sampling, annotation, analysis |
| `data/` | Sampled instance IDs (no text) |
| `results/` | Statistics and figures |

## Notebooks

1. `01_eda.ipynb` – exploratory data analysis of English POLAR
2. `02_sampling.ipynb` – balanced sampling of 300 instances

## Status

- [x] Repository and Overleaf set up
- [x] Exploratory data analysis
- [x] Sampling (300 instances)
- [ ] Annotation guidelines
- [ ] Human annotation (3 × 300)
- [ ] LLM annotation
- [ ] Analysis and error analysis
- [ ] Final report