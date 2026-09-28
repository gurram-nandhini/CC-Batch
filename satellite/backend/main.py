from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import os
import io

app = FastAPI(
    title="Satellite Image Analysis API",
    description="API for uploading and analyzing satellite images",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Satellite Image Analysis API is running"
    }


# ---------------------------------------------------
# IMAGE UPLOAD
# ---------------------------------------------------

@app.post("/image/upload")
async def upload_image(file: UploadFile = File(...)):

    try:
        contents = await file.read()

        image = Image.open(io.BytesIO(contents))

        width, height = image.size

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as f:
            f.write(contents)

        return {
            "success": True,
            "filename": file.filename,
            "width": width,
            "height": height,
            "format": image.format,
            "message": "Satellite image uploaded successfully"
        }

    except Exception:
        return {
            "success": False,
            "message": "Invalid image file"
        }


# ---------------------------------------------------
# IMAGE ANALYSIS
# ---------------------------------------------------

@app.post("/image/analyze")
async def analyze_image(file: UploadFile = File(...)):

    try:

        contents = await file.read()

        image = Image.open(
            io.BytesIO(contents)
        )

        # Convert image to RGB
        image = image.convert("RGB")

        width, height = image.size

        # Get pixel data
        pixels = list(image.getdata())

        total_pixels = len(pixels)

        # Calculate RGB averages
        total_red = sum(pixel[0] for pixel in pixels)
        total_green = sum(pixel[1] for pixel in pixels)
        total_blue = sum(pixel[2] for pixel in pixels)

        average_red = total_red / total_pixels
        average_green = total_green / total_pixels
        average_blue = total_blue / total_pixels

        # Calculate brightness
        brightness = (
            0.299 * average_red
            + 0.587 * average_green
            + 0.114 * average_blue
        )

        # Simple brightness classification
        if brightness < 70:
            brightness_level = "Dark"
        elif brightness < 170:
            brightness_level = "Moderate"
        else:
            brightness_level = "Bright"

        return {
            "success": True,

            "filename": file.filename,

            "image": {
                "width": width,
                "height": height,
                "format": image.format
            },

            "rgb": {
                "average_red": round(average_red, 2),
                "average_green": round(average_green, 2),
                "average_blue": round(average_blue, 2)
            },

            "brightness": {
                "value": round(brightness, 2),
                "level": brightness_level
            },

            "message": "Satellite image analyzed successfully"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }