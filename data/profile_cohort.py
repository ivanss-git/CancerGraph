import pandas as pd

from build_shared_cohort import load_processed_cohort


clinical_shared, mirna_shared, mrna_shared = load_processed_cohort()


def check_duplicates():
    duplicate_samples = clinical_shared[
        clinical_shared.duplicated("SAMPLE_ID", keep=False)
    ]

    duplicate_patients = clinical_shared[
        clinical_shared.duplicated("PATIENT_ID", keep=False)
    ]

    duplicate_mrna = mrna_shared[
        mrna_shared.duplicated(
            subset=list(mrna_shared.columns[:2]),
            keep=False,
        )
    ].sort_values(list(mrna_shared.columns[:2]))

    print("Duplicate SAMPLE_ID rows:", len(duplicate_samples))
    print("Patients with multiple samples:", len(duplicate_patients))

    print(
        "Duplicate miRNA sample columns:",
        pd.Index(mirna_shared.columns[2:]).duplicated().sum(),
    )

    print(
        "Duplicate mRNA sample columns:",
        pd.Index(mrna_shared.columns[2:]).duplicated().sum(),
    )

    print(
        "Duplicate miRNA feature IDs:",
        mirna_shared.iloc[:, 0].duplicated().sum(),
    )

    print(
        "Duplicate mRNA feature IDs:",
        mrna_shared.iloc[:, 0].duplicated().sum(),
    )

    if not duplicate_mrna.empty:
        print("\nDuplicated mRNA identifiers:")
        print(duplicate_mrna.iloc[:, :2])


if __name__ == "__main__":
    check_duplicates()