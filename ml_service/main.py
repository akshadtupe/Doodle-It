from fastapi import FastAPI
import time

app = FastAPI()

@app.post("/generate")
def generate(data: dict):

    style = data.get("style")  
    print("ML service generating image...", style)

    time.sleep(2)   #fake AI thinking

    return {
        "image": "https://picsum.photos/500"
    }