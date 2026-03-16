from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {
        "status": "backend running",
        "ml_service": os.getenv("ML_URL")
    }


class DoodleInput(BaseModel):
    image: str

@app.post("/generate")
def generate(data: DoodleInput):
    print("Received doodle")

    return {
        "message": "image received",
        "preview": data.image
    }