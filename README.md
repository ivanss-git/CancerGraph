# CancerGraph

CancerGraph is an end-to-end cancer bioinformatics and machine-learning research project focused initially on breast cancer. It aims to predict and rank meaningful miRNA–cancer associations using miRNA expression, gene expression, biological relationships, and clinical data.

## Current Progress

- Collected TCGA breast cancer data from cBioPortal
- Matched clinical, miRNA, and mRNA data
- Created a shared cohort of 298 samples
- Added a reproducible data-alignment pipeline

## Project Structure

- `data/` — Raw and processed data pipelines
- `database/` — PostgreSQL schema and migrations
- `notebooks/` — Data exploration and experiments
- `src/` — Application and model source code
- `tests/` — Automated tests

## Run the Data Pipeline

Place the required TCGA files in `data/raw/`, then run:

```bash
python data/build_shared_cohort.py