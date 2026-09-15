from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def build_shared_cohort():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    clinical = pd.read_csv(
        RAW_DIR / "clinical_data.tsv",
        sep="\t",
        comment="#",
    )

    mirna = pd.read_csv(
        RAW_DIR / "mirna_expression.tsv",
        sep="\t",
        comment="#",
    )

    mrna = pd.read_csv(
        RAW_DIR / "mrna_expression.tsv",
        sep="\t",
        comment="#",
    )

    clinical_ids = set(clinical["SAMPLE_ID"].dropna())
    mirna_ids = set(mirna.columns[2:])
    mrna_ids = set(mrna.columns[2:])

    shared_ids = sorted(
        clinical_ids & mirna_ids & mrna_ids
    )

    clinical_shared = clinical[
        clinical["SAMPLE_ID"].isin(shared_ids)
    ].copy()

    mirna_shared = mirna[
        list(mirna.columns[:2]) + shared_ids
    ].copy()

    mrna_shared = mrna[
        list(mrna.columns[:2]) + shared_ids
    ].copy()

    clinical_shared.to_csv(
        PROCESSED_DIR / "clinical_shared.tsv",
        sep="\t",
        index=False,
    )

    mirna_shared.to_csv(
        PROCESSED_DIR / "mirna_shared.tsv",
        sep="\t",
        index=False,
    )

    mrna_shared.to_csv(
        PROCESSED_DIR / "mrna_shared.tsv",
        sep="\t",
        index=False,
    )

    print("Clinical samples:", len(clinical_ids))
    print("miRNA samples:", len(mirna_ids))
    print("mRNA samples:", len(mrna_ids))
    print("Shared samples:", len(shared_ids))

    print("\nSaved processed data:")
    print("Clinical shape:", clinical_shared.shape)
    print("miRNA shape:", mirna_shared.shape)
    print("mRNA shape:", mrna_shared.shape)
    print("Location:", PROCESSED_DIR)

    assert len(shared_ids) == len(clinical_shared)
    assert set(clinical_shared["SAMPLE_ID"]) == set(shared_ids)
    assert set(mirna_shared.columns[2:]) == set(shared_ids)
    assert set(mrna_shared.columns[2:]) == set(shared_ids)

    print("\nValidation passed: all datasets use the same cohort.")

    return clinical_shared, mirna_shared, mrna_shared


def load_processed_cohort():
    clinical = pd.read_csv(
        PROCESSED_DIR / "clinical_shared.tsv",
        sep="\t",
    )

    mirna = pd.read_csv(
        PROCESSED_DIR / "mirna_shared.tsv",
        sep="\t",
    )

    mrna = pd.read_csv(
        PROCESSED_DIR / "mrna_shared.tsv",
        sep="\t",
    )

    return clinical, mirna, mrna


if __name__ == "__main__":
    build_shared_cohort()