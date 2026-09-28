import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "datasets" / "TCGA-PANCAN-HiSeq-801x20531"

DATA_PATH = DATA_DIR / "data.csv"
LABEL_PATH = DATA_DIR / "labels.csv"

MODEL_FOLDER = BASE_DIR / "models"

# Create models folder automatically
MODEL_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. CHECK DATASET
# ============================================================

print("=" * 70)
print("GENE EXPRESSION CANCER MODEL TRAINING")
print("=" * 70)

print("\nChecking dataset files...")

print("Data file:")
print(DATA_PATH)

print("\nLabels file:")
print(LABEL_PATH)


if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Data file not found:\n{DATA_PATH}"
    )


if not LABEL_PATH.exists():
    raise FileNotFoundError(
        f"Labels file not found:\n{LABEL_PATH}"
    )


print("\nDataset files found successfully!")


# ============================================================
# 3. LOAD DATA
# ============================================================

print("\n" + "=" * 70)
print("LOADING DATA")
print("=" * 70)

data = pd.read_csv(DATA_PATH)

labels = pd.read_csv(LABEL_PATH)


print("\nData shape:")
print(data.shape)

print("\nLabels shape:")
print(labels.shape)

print("\nData columns:")
print(data.columns[:10].tolist())

print("\nLabels columns:")
print(labels.columns.tolist())


# ============================================================
# 4. REMOVE INDEX / ID COLUMNS
# ============================================================

print("\n" + "=" * 70)
print("PREPARING DATA")
print("=" * 70)


# Remove automatically-created unnamed columns
data = data.loc[
    :,
    ~data.columns.str.contains(
        "^Unnamed",
        case=False
    )
]

labels = labels.loc[
    :,
    ~labels.columns.str.contains(
        "^Unnamed",
        case=False
    )
]


# Detect possible ID column
possible_id_columns = [
    "sample",
    "sample_id",
    "Sample",
    "Sample_ID",
    "id",
    "ID",
    "barcode"
]


data_id_column = None
label_id_column = None


for column in possible_id_columns:

    if column in data.columns:
        data_id_column = column
        break


for column in possible_id_columns:

    if column in labels.columns:
        label_id_column = column
        break


# Also check first column if it is non-numeric
if data_id_column is None:

    first_column = data.columns[0]

    if not pd.api.types.is_numeric_dtype(
        data[first_column]
    ):
        data_id_column = first_column


if label_id_column is None:

    first_column = labels.columns[0]

    if not pd.api.types.is_numeric_dtype(
        labels[first_column]
    ):
        label_id_column = first_column


print("\nDetected data ID column:")
print(data_id_column)

print("\nDetected label ID column:")
print(label_id_column)


# ============================================================
# 5. ALIGN DATA AND LABELS
# ============================================================

if (
    data_id_column is not None
    and label_id_column is not None
):

    print("\nAligning samples using sample IDs...")

    data[data_id_column] = (
        data[data_id_column]
        .astype(str)
    )

    labels[label_id_column] = (
        labels[label_id_column]
        .astype(str)
    )

    merged = pd.merge(
        data,
        labels,
        left_on=data_id_column,
        right_on=label_id_column,
        how="inner"
    )

    print(
        "Matched samples:",
        len(merged)
    )

    # Gene-expression columns
    gene_columns = [
        column
        for column in data.columns
        if column != data_id_column
        and pd.api.types.is_numeric_dtype(
            data[column]
        )
    ]

    X = merged[gene_columns].copy()

    # Find label column
    label_candidates = [
        column
        for column in labels.columns
        if column != label_id_column
    ]

    if len(label_candidates) == 0:

        raise ValueError(
            "No label column found in labels.csv"
        )

    target_column = label_candidates[0]

    y = merged[target_column].copy()


else:

    print(
        "\nSample ID columns were not detected."
    )

    print(
        "Using row-by-row alignment..."
    )

    # Find numeric gene columns
    gene_columns = [
        column
        for column in data.columns
        if pd.api.types.is_numeric_dtype(
            data[column]
        )
    ]

    X = data[gene_columns].copy()

    # Find target column
    label_candidates = [
        column
        for column in labels.columns
        if not pd.api.types.is_numeric_dtype(
            labels[column]
        )
        or labels[column].nunique() < 50
    ]

    if len(label_candidates) == 0:

        # Use last column as fallback
        target_column = labels.columns[-1]

    else:

        target_column = label_candidates[-1]

    y = labels[target_column].copy()


print("\nTarget column:")
print(target_column)

print("\nNumber of gene features:")
print(len(gene_columns))

print("\nNumber of samples:")
print(len(X))


# ============================================================
# 6. CLEAN DATA
# ============================================================

print("\n" + "=" * 70)
print("CLEANING DATA")
print("=" * 70)


# Convert genes to numeric
X = X.apply(
    pd.to_numeric,
    errors="coerce"
)


# Replace infinity
X = X.replace(
    [np.inf, -np.inf],
    np.nan
)


# Fill missing gene values
X = X.fillna(
    X.median()
)


# Remove constant columns
constant_columns = [
    column
    for column in X.columns
    if X[column].nunique() <= 1
]


if constant_columns:

    print(
        "\nRemoving constant columns:",
        len(constant_columns)
    )

    X = X.drop(
        columns=constant_columns
    )


# Remove missing labels
valid_rows = y.notna()

X = X.loc[valid_rows].reset_index(
    drop=True
)

y = y.loc[valid_rows].reset_index(
    drop=True
)


print("\nFinal X shape:")
print(X.shape)

print("\nFinal y shape:")
print(y.shape)


# ============================================================
# 7. ENCODE LABELS
# ============================================================

print("\n" + "=" * 70)
print("ENCODING CANCER LABELS")
print("=" * 70)


label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(
    y.astype(str)
)


print("\nCancer classes:")

for number, name in enumerate(
    label_encoder.classes_
):

    print(
        number,
        "->",
        name
    )


# ============================================================
# 8. TRAIN / TEST SPLIT
# ============================================================

print("\n" + "=" * 70)
print("TRAIN / TEST SPLIT")
print("=" * 70)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)


print("\nTraining samples:")
print(len(X_train))

print("\nTesting samples:")
print(len(X_test))


# ============================================================
# 9. FEATURE SELECTION
# ============================================================

print("\n" + "=" * 70)
print("FEATURE SELECTION")
print("=" * 70)


# Select the most important genes
K_FEATURES = min(
    500,
    X_train.shape[1]
)


selector = SelectKBest(
    score_func=f_classif,
    k=K_FEATURES
)


X_train_selected = selector.fit_transform(
    X_train,
    y_train
)

X_test_selected = selector.transform(
    X_test
)


print(
    "\nSelected gene features:",
    K_FEATURES
)


# ============================================================
# 10. SCALING
# ============================================================

print("\n" + "=" * 70)
print("FEATURE SCALING")
print("=" * 70)


scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train_selected
)

X_test_scaled = scaler.transform(
    X_test_selected
)


# ============================================================
# 11. PCA
# ============================================================

print("\n" + "=" * 70)
print("PCA DIMENSION REDUCTION")
print("=" * 70)


N_COMPONENTS = min(
    50,
    X_train_scaled.shape[0] - 1,
    X_train_scaled.shape[1]
)


pca = PCA(
    n_components=N_COMPONENTS,
    random_state=42
)


X_train_pca = pca.fit_transform(
    X_train_scaled
)

X_test_pca = pca.transform(
    X_test_scaled
)


print(
    "\nPCA components:",
    N_COMPONENTS
)

print(
    "Explained variance:",
    round(
        pca.explained_variance_ratio_.sum() * 100,
        2
    ),
    "%"
)


# ============================================================
# 12. TRAIN MODEL
# ============================================================

print("\n" + "=" * 70)
print("TRAINING LOGISTIC REGRESSION")
print("=" * 70)


model = LogisticRegression(
    max_iter=5000,
    random_state=42
)


model.fit(
    X_train_pca,
    y_train
)


# ============================================================
# 13. EVALUATION
# ============================================================

print("\n" + "=" * 70)
print("MODEL EVALUATION")
print("=" * 70)


predictions = model.predict(
    X_test_pca
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    "\nModel Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)


# ============================================================
# 14. SAVE FEATURE INFORMATION
# ============================================================

selected_gene_mask = selector.get_support()

selected_gene_names = X.columns[
    selected_gene_mask
].tolist()


# ============================================================
# 15. SAVE ALL MODEL FILES
# ============================================================

print("\n" + "=" * 70)
print("SAVING MODEL FILES")
print("=" * 70)


# Original feature columns
joblib.dump(
    X.columns.tolist(),
    MODEL_FOLDER / "feature_columns.pkl"
)


# Selected genes
joblib.dump(
    selected_gene_names,
    MODEL_FOLDER / "selected_genes.pkl"
)


# Feature selector
joblib.dump(
    selector,
    MODEL_FOLDER / "gene_selector.pkl"
)


# Scaler
joblib.dump(
    scaler,
    MODEL_FOLDER / "gene_scaler.pkl"
)


# PCA
joblib.dump(
    pca,
    MODEL_FOLDER / "gene_pca.pkl"
)


# ML model
joblib.dump(
    model,
    MODEL_FOLDER / "gene_model.pkl"
)


# Label encoder
joblib.dump(
    label_encoder,
    MODEL_FOLDER / "label_encoder.pkl"
)


print("\nModel files saved successfully!")

print("\nLocation:")

print(
    MODEL_FOLDER
)


# ============================================================
# 16. DISPLAY SAVED FILES
# ============================================================

print("\nSaved files:")

for file in MODEL_FOLDER.iterdir():

    print(
        "✓",
        file.name
    )


print("\n" + "=" * 70)
print("TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 70)