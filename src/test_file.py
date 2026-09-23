import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))

from data.build_shared_cohort import load_processed_cohort

clinical, mirna, mrna = load_processed_cohort()

print("Clinical:", clinical.shape)
print("miRNA:", mirna.shape)
print("mRNA:", mrna.shape)