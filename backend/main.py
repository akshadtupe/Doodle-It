from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
import httpx

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class DoodleInput(BaseModel):
    image: str
    style: str

@app.post("/generate")
async def generate(data: DoodleInput):
    print("backend Received doodle")
    print("Doodle style:", data.style)  

    async with httpx.AsyncClient() as client:
        res=await client.post(
            "http://localhost:8001/generate",
            json={
                "image": data.image,
                "style": data.style
            }
        )

    ml_response = res.json()
    print("Received from ML service:", ml_response)

    return {
        "preview": ml_response["image"]
    }

