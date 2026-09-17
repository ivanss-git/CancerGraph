# CancerGraph

CancerGraph is a research project exploring relationships between **miRNA expression, mRNA expression, and breast cancer clinical data** using the TCGA Breast Cancer (BRCA) cohort.

The long-term goal is to develop machine learning and graph-based methods for identifying biologically meaningful miRNA–gene relationships and potential cancer biomarkers.

## Current Progress

- Collected TCGA BRCA clinical, miRNA, and mRNA expression data
- Identified and validated a shared patient/sample cohort across all three datasets
- Built a preprocessing pipeline for aligning the datasets
- Generated processed clinical, miRNA, and mRNA cohort files
- Added cohort profiling and exploratory analysis
- Created an initial PostgreSQL database schema and migration structure
- Set up project modules for future graph construction, modeling, and experimentation

## Project Structure

```text
CancerGraph/
├── data/
│   ├── raw/                 # Raw clinical and expression datasets
│   ├── processed/           # Aligned shared-cohort datasets
│   ├── build_shared_cohort.py
│   └── profile_cohort.py
├── database/
│   └── migrations/          # PostgreSQL schema migrations
├── notebooks/               # Exploratory analysis
├── src/cancergraph/
│   ├── data/                # Data processing
│   ├── graph/               # Graph construction
│   ├── models/              # Machine learning models
│   ├── telemetry/           # Experiment tracing
│   └── utils/
├── tests/
├── docker-compose.yml
└── README.md
```

## Research Direction

The next stages of the project will focus on preprocessing and normalizing molecular features, constructing miRNA–gene interaction representations, establishing baseline machine learning models, and eventually evaluating graph-based and neural network approaches for discovering candidate cancer-related relationships.

## Data

The project currently uses the **TCGA Breast Cancer (BRCA)** dataset, including:

- Clinical information
- miRNA expression
- mRNA expression

## Status

**Active research / early development.**

The current focus is building a reliable data pipeline and understanding the cohort before moving into predictive modeling and biological validation.
