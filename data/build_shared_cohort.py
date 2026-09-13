from pathlib import Path

import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load raw data
# --------------------------------------------------

clinical = pd.read_csv(
    RAW_DIR / "clinical_data.tsv",
    sep="\t",
    comment="#"
)

mirna = pd.read_csv(
    RAW_DIR / "mirna_expression.tsv",
    sep="\t",
    comment="#"
)

mrna = pd.read_csv(
    RAW_DIR / "mrna_expression.tsv",
    sep="\t",
    comment="#"
)


# --------------------------------------------------
# Find shared samples
# --------------------------------------------------

clinical_ids = set(clinical["SAMPLE_ID"].dropna())
mirna_ids = set(mirna.columns[2:])
mrna_ids = set(mrna.columns[2:])

shared_ids = sorted(
    clinical_ids & mirna_ids & mrna_ids
)

print("Clinical samples:", len(clinical_ids))
print("miRNA samples:", len(mirna_ids))
print("mRNA samples:", len(mrna_ids))
print("Shared samples:", len(shared_ids))


# --------------------------------------------------
# Filter to shared cohort
# --------------------------------------------------

clinical_shared = clinical[
    clinical["SAMPLE_ID"].isin(shared_ids)
].copy()

mirna_shared = mirna[
    list(mirna.columns[:2]) + shared_ids
].copy()

mrna_shared = mrna[
    list(mrna.columns[:2]) + shared_ids
].copy()


# --------------------------------------------------
# Save processed data
# --------------------------------------------------

clinical_shared.to_csv(
    PROCESSED_DIR / "clinical_shared.tsv",
    sep="\t",
    index=False
)

mirna_shared.to_csv(
    PROCESSED_DIR / "mirna_shared.tsv",
    sep="\t",
    index=False
)

mrna_shared.to_csv(
    PROCESSED_DIR / "mrna_shared.tsv",
    sep="\t",
    index=False
)

print("\nSaved processed data:")
print("Clinical shape:", clinical_shared.shape)
print("miRNA shape:", mirna_shared.shape)
print("mRNA shape:", mrna_shared.shape)
print("Location:", PROCESSED_DIR)


# --------------------------------------------------
# Inspect clinical data
# --------------------------------------------------

print("\nClinical columns:")
print(clinical_shared.columns.tolist())

preferred_columns = [
    "SAMPLE_ID",
    "PATIENT_ID",
    "ER_STATUS",
    "HER2_STATUS",
    "PR_STATUS",
    "PAM50_SUBTYPE",
    "TUMOR_STAGE",
    "SAMPLE_TYPE",
]

available_columns = [
    column
    for column in preferred_columns
    if column in clinical_shared.columns
]

print("\nAvailable useful columns:")
print(available_columns)

print("\nMissing values:")
print(clinical_shared[available_columns].isna().sum())


# --------------------------------------------------
# Inspect prediction-label distributions
# --------------------------------------------------

candidate_labels = [
    "PAM50_SUBTYPE",
    "ER_STATUS",
    "HER2_STATUS",
    "PR_STATUS",
    "TUMOR_STAGE",
]

for column in candidate_labels:
    if column in clinical_shared.columns:
        print(f"\n{column} distribution:")
        print(clinical_shared[column].value_counts(dropna=False))


# --------------------------------------------------
# Validate saved cohort
# --------------------------------------------------

assert len(shared_ids) == len(clinical_shared)
assert set(clinical_shared["SAMPLE_ID"]) == set(shared_ids)
assert set(mirna_shared.columns[2:]) == set(shared_ids)
assert set(mrna_shared.columns[2:]) == set(shared_ids)

print("\nValidation passed: all three datasets use the same cohort.")