from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union
import pandas as pd
import io

from ml_model import predict_gene_expression
from database import get_connection

router = APIRouter(prefix="/prediction", tags=["Prediction"])


# ---------------------------------------------------------
# CSV PREDICTION
# ---------------------------------------------------------
@router.post("/csv")
async def predict_from_csv(
    user_id: int = Form(...),
    sample_name: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Check file type
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are allowed"
            )

        # Read uploaded CSV
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded CSV file is empty"
            )

        df = pd.read_csv(io.BytesIO(contents))

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="CSV file contains no data"
            )

        # -------------------------------------------------
        # Use first row for prediction
        # -------------------------------------------------
        row = df.iloc[0]

        # Convert row into dictionary
        gene_values = row.to_dict()

        # Remove possible sample/id columns
        remove_columns = [
            "id",
            "ID",
            "sample",
            "Sample",
            "sample_id",
            "Sample_ID"
        ]

        for column in remove_columns:
            gene_values.pop(column, None)

        # Make prediction
        prediction_result = predict_gene_expression(gene_values)

        # Handle tuple/dict result
        if isinstance(prediction_result, tuple):
            prediction = prediction_result[0]
            probability = prediction_result[1]
        elif isinstance(prediction_result, dict):
            prediction = (
                prediction_result.get("prediction")
                or prediction_result.get("cancer_type")
                or prediction_result.get("label")
                or "Unknown"
            )

            probability = prediction_result.get(
                "probability",
                0
            )
        else:
            prediction = str(prediction_result)
            probability = 0

        # Convert probability safely
        try:
            probability = float(probability)
        except (TypeError, ValueError):
            probability = 0.0

        # -------------------------------------------------
        # Save prediction in MySQL
        # -------------------------------------------------
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO predictions
            (user_id, sample_name, prediction, probability)
            VALUES (%s, %s, %s, %s)
            """,
            (
                user_id,
                sample_name,
                prediction,
                probability
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "success": True,
            "sample_name": sample_name,
            "prediction": prediction,
            "probability": probability
        }

    except HTTPException:
        raise

    except Exception as e:
        print("CSV PREDICTION ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------------
# EXISTING JSON PREDICTION
# ---------------------------------------------------------
class GenePredictionRequest(BaseModel):
    sample_name: str
    user_id: int
    gene_values: Union[List[float], Dict[str, float]]


@router.post("/")
def predict_gene(request: GenePredictionRequest):

    try:
        result = predict_gene_expression(
            request.gene_values
        )

        if isinstance(result, tuple):
            prediction = result[0]
            probability = result[1]
        elif isinstance(result, dict):
            prediction = result.get(
                "prediction",
                result.get("label", "Unknown")
            )
            probability = result.get(
                "probability",
                0
            )
        else:
            prediction = str(result)
            probability = 0

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO predictions
            (user_id, sample_name, prediction, probability)
            VALUES (%s, %s, %s, %s)
            """,
            (
                request.user_id,
                request.sample_name,
                prediction,
                float(probability)
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "success": True,
            "sample_name": request.sample_name,
            "prediction": prediction,
            "probability": float(probability)
        }

    except Exception as e:
        print("PREDICTION ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------------
# HISTORY
# ---------------------------------------------------------
@router.get("/history/{user_id}")
def get_prediction_history(user_id: int):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            sample_name,
            prediction,
            probability,
            created_at
        FROM predictions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results