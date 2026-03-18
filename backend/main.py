from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
import httpx
from fastapi import UploadFile, File, Form


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
async def generate( file:UploadFile = File(...), style:str = Form(...) ):

    print("Received file:", file.filename)
    print("Doodle style:", style)  

    async with httpx.AsyncClient(timeout=None) as client:
        res=await client.post(
            "http://localhost:8001/generate",
            files={"file": await file.read()},
            data={"style": style}
        )

    ml_response = res.json()
    

    return {
        "preview": ml_response["image"]
    }

