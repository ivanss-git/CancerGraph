import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data.build_shared_cohort import load_processed_cohort


def build_association_matrix():

    _, mirna_shared, mrna_shared = load_processed_cohort()

    # Small subset first for testing
    mirna_shared = mirna_shared.head(5)
    mrna_shared = mrna_shared.head(5)

    mirna_names = mirna_shared.iloc[:, 0].astype(str)
    gene_names = mrna_shared.iloc[:, 0].astype(str)

    num_mirnas = len(mirna_shared)
    num_genes = len(mrna_shared)

    Y = np.zeros((num_mirnas, num_genes))

    for i in range(num_mirnas):

        mirna_values = (
            mirna_shared.iloc[i, 2:]
            .astype(float)
            .values
        )

        for j in range(num_genes):

            gene_values = (
                mrna_shared.iloc[j, 2:]
                .astype(float)
                .values
            )

            corr = np.corrcoef(
                mirna_values,
                gene_values
            )[0, 1]

            if np.isnan(corr):
                corr = 0.0

            corr = np.clip(corr, -1.0, 1.0)

            Y[i, j] = corr

    association_df = pd.DataFrame(
        Y,
        index=mirna_names,
        columns=gene_names,
    )

    print("\nAssociation Matrix:")
    print(association_df)

    return association_df


if __name__ == "__main__":
    build_association_matrix()

# 5x5 tests for association across 298 
# removing the 5 head statements would give the full list
# we want to add that into a database using postgres
# uses 398 miRNAs and 17268 genes
# so y is the association for miRNAs an Genes (edges), 
# now we need the nodes for miRNAs and Genes to build the graph
#  