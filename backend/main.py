from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "backend running",
        "ml_service": os.getenv("ML_URL")
    }