import pandas as pd
from pathlib import Path


print("=" * 60)
print("GENE EXPRESSION DATASET INSPECTION")
print("=" * 60)


# --------------------------------------------------
# 1. Dataset folder
# --------------------------------------------------

DATASET_FOLDER = Path("datasets")

print("\nSearching for CSV files...")


# Find all CSV files inside datasets
csv_files = list(DATASET_FOLDER.rglob("*.csv"))


print("\nCSV files found:")

for file in csv_files:
    print(" -", file)


# --------------------------------------------------
# 2. Find data.csv and labels.csv
# --------------------------------------------------

data_files = [
    file for file in csv_files
    if file.name.lower() == "data.csv"
]

label_files = [
    file for file in csv_files
    if file.name.lower() == "labels.csv"
]


if not data_files:
    print("\nERROR: data.csv was not found.")
    exit()


if not label_files:
    print("\nERROR: labels.csv was not found.")
    exit()


DATA_PATH = data_files[0]
LABEL_PATH = label_files[0]


print("\nData file:")
print(DATA_PATH)

print("\nLabels file:")
print(LABEL_PATH)


# --------------------------------------------------
# 3. Load datasets
# --------------------------------------------------

print("\nLoading data...")

data = pd.read_csv(DATA_PATH)

labels = pd.read_csv(LABEL_PATH)


# --------------------------------------------------
# 4. Dataset shape
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print("\nGene expression data shape:")
print(data.shape)

print("\nLabels shape:")
print(labels.shape)


# --------------------------------------------------
# 5. Data columns
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA COLUMNS")
print("=" * 60)

print("\nFirst 10 columns:")

print(data.columns[:10].tolist())


# --------------------------------------------------
# 6. First rows
# --------------------------------------------------

print("\nFirst 5 rows of gene expression data:")

print(data.head())


print("\nFirst 10 rows of labels:")

print(labels.head(10))


# --------------------------------------------------
# 7. Label columns
# --------------------------------------------------

print("\n" + "=" * 60)
print("LABEL INFORMATION")
print("=" * 60)

print("\nLabel columns:")

print(labels.columns.tolist())


for column in labels.columns:

    print("\nColumn:", column)

    print(labels[column].value_counts())


# --------------------------------------------------
# 8. Data types
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)

print(data.dtypes.value_counts())


# --------------------------------------------------
# 9. Missing values
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print(
    "Missing values in data:",
    data.isnull().sum().sum()
)

print(
    "Missing values in labels:",
    labels.isnull().sum().sum()
)


# --------------------------------------------------
# 10. Duplicate rows
# --------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATES")
print("=" * 60)

print(
    "Duplicate rows in data:",
    data.duplicated().sum()
)

print(
    "Duplicate rows in labels:",
    labels.duplicated().sum()
)


print("\n" + "=" * 60)
print("INSPECTION COMPLETED")
print("=" * 60)