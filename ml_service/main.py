from fastapi import FastAPI
import time
from fastapi import UploadFile, File, Form
from diffusers import StableDiffusionPipeline
import torch
import uuid
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


#outputdir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")


#Load Model
model="runwayml/stable-diffusion-v1-5"
print("Loading SD Model....")

pipe= StableDiffusionPipeline.from_pretrained(
    model
)

device = "cpu"
pipe = pipe.to(device)

#memory efficient attention
# pipe.enable_attention_slicing()

print(f"Model loaded on {device} successfully!")

@app.post("/generate")
def generate( file:UploadFile = File(...), style:str = Form(...) ):
    
    print("Generating image with style:", style)

    prompt= f"{style}, cat image"

    image= pipe(prompt,
                height=384,
                width=384,
                guidance_scale=7.5
                ).images[0]
    

    filename= f"gen_{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)


    image.save(filepath)

    return{
        "image":f"http://127.0.0.1:8001/outputs/{filename}"
    }


