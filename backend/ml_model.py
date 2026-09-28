import joblib
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# MODEL PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_FOLDER = BASE_DIR / "models"


# ============================================================
# LOAD TRAINED MODELS
# ============================================================

feature_columns = joblib.load(
    MODEL_FOLDER / "feature_columns.pkl"
)

selected_genes = joblib.load(
    MODEL_FOLDER / "selected_genes.pkl"
)

gene_selector = joblib.load(
    MODEL_FOLDER / "gene_selector.pkl"
)

gene_scaler = joblib.load(
    MODEL_FOLDER / "gene_scaler.pkl"
)

gene_pca = joblib.load(
    MODEL_FOLDER / "gene_pca.pkl"
)

gene_model = joblib.load(
    MODEL_FOLDER / "gene_model.pkl"
)

label_encoder = joblib.load(
    MODEL_FOLDER / "label_encoder.pkl"
)


print("========================================")
print("GENE EXPRESSION MODEL LOADED")
print("========================================")
print("Features:", len(feature_columns))
print("Selected genes:", len(selected_genes))
print("Model:", type(gene_model).__name__)
print("========================================")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_gene_expression(gene_values):

    try:

        # ----------------------------------------------------
        # Convert input to DataFrame
        # ----------------------------------------------------

        if isinstance(gene_values, dict):

            df = pd.DataFrame([gene_values])

        elif isinstance(gene_values, list):

            if len(gene_values) != len(feature_columns):

                raise ValueError(
                    f"Expected {len(feature_columns)} gene values, "
                    f"but received {len(gene_values)}"
                )

            df = pd.DataFrame(
                [gene_values],
                columns=feature_columns
            )

        else:

            raise ValueError(
                "Gene expression data must be a list or dictionary"
            )


        # ----------------------------------------------------
        # Make sure all required features exist
        # ----------------------------------------------------

        df = df.reindex(
            columns=feature_columns,
            fill_value=0
        )


        # ----------------------------------------------------
        # Convert values to numeric
        # ----------------------------------------------------

        df = df.apply(
            pd.to_numeric,
            errors="coerce"
        )

        df = df.fillna(0)


        # ----------------------------------------------------
        # Gene Selection
        # ----------------------------------------------------

        X = gene_selector.transform(df)


        # ----------------------------------------------------
        # Scaling
        # ----------------------------------------------------

        X = gene_scaler.transform(X)


        # ----------------------------------------------------
        # PCA
        # ----------------------------------------------------

        X = gene_pca.transform(X)


        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = gene_model.predict(X)[0]


        # ----------------------------------------------------
        # Convert encoded label to cancer type
        # ----------------------------------------------------

        try:

            prediction_label = label_encoder.inverse_transform(
                [prediction]
            )[0]

        except Exception:

            prediction_label = str(prediction)


        # ----------------------------------------------------
        # Probability
        # ----------------------------------------------------

        probability = None

        if hasattr(
            gene_model,
            "predict_proba"
        ):

            probabilities = gene_model.predict_proba(X)[0]

            probability = float(
                np.max(probabilities) * 100
            )


        # ----------------------------------------------------
        # Result
        # ----------------------------------------------------

        return {
            "prediction": str(prediction_label),
            "probability": (
                round(probability, 2)
                if probability is not None
                else None
            )
        }


    except Exception as e:

        raise ValueError(
            f"Gene prediction failed: {str(e)}"
        )