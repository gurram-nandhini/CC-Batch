from fastapi import APIRouter, UploadFile, File, HTTPException

import pandas as pd
import os


# Create router
router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"]
)


# Upload folder
UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...)
):

    # Check file type
    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )


    # Create file path
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )


    # Read uploaded file
    contents = await file.read()


    # Save file
    with open(
        file_path,
        "wb"
    ) as f:

        f.write(contents)


    # Read CSV
    df = pd.read_csv(
        file_path
    )


    return {
        "message": "Dataset uploaded successfully",
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns)
    }