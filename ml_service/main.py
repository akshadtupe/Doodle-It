from fastapi import FastAPI
import time
from fastapi import UploadFile, File, Form

app = FastAPI()

@app.post("/generate")
def generate( file:UploadFile = File(...), style:str = Form(...) ):

    print("Ml received file:", file.filename)
    print("Ml received style:", style)

    return {
        "image": f"https://picsum.photos/seed/{style}/500"
    }