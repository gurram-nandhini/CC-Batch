from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.dataset_routes import router as dataset_router
from routes.prediction_routes import router as prediction_router

app = FastAPI(
    title="Gene Expression Cancer Analysis API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(dataset_router)
app.include_router(prediction_router)


@app.get("/")
def home():
    return {
        "message": "Gene Expression Cancer Analysis API is running"
    }