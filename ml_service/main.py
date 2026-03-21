from fastapi import FastAPI
import time
from fastapi import UploadFile, File, Form
from diffusers import StableDiffusionPipeline
import torch
import uuid
from fastapi.staticfiles import StaticFiles
import os
import numpy as np
import cv2
from PIL import Image
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline, StableDiffusionControlNetImg2ImgPipeline

#APP
app = FastAPI()


#Output Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")


#DEVICE
device = "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32


#Load controlNet Model [Scribble + Canny]
print("Loading ControlNet Models....")

controlnet= ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-scribble",
    torch_dtype=dtype
)

canny_controlnet= ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny",
    torch_dtype=dtype
)
print("Both ControlNet Models loaded successfully!")

#Load img2img + ControlNet Pipeline

pipe= StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=[controlnet, canny_controlnet],
    torch_dtype=dtype,
    safety_checker=None
)

pipe= pipe.to(device)

#memory efficient attention
pipe.enable_attention_slicing()
print(f"Pipeline ready on {device}")



#Endpoint
@app.post("/generate")
async def generate( file:UploadFile = File(...), style:str = Form(...) ):

    print("Generating image with style:", style)

    #Read doodle file 
    contents = file.file.read()

    #Convert raw bytes to numpy array
    np_img = np.frombuffer(contents, np.uint8)

    #Decode image (PNG to  BGR image)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)


    #Resize for SD
    img = cv2.resize(img, (512, 512))


    #Color hint
    blur = cv2.GaussianBlur(img, (41, 41), 0)

    color_pil = Image.fromarray(
        cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    )


    ##Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #Scribble map
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((5, 5), np.uint8)

    scribble = cv2.dilate(thresh, kernel, iterations=2)

    scribble_rgb = cv2.cvtColor(scribble, cv2.COLOR_GRAY2RGB)

    scribble_pil = Image.fromarray(scribble_rgb)


    #Cnny map (HARD geometry)
    edges = cv2.Canny(gray, 30, 100)

    edge_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    canny_pil = Image.fromarray(edge_rgb)


    #Save debug
    scribble_pil.save(os.path.join(OUTPUT_DIR, "scribble_debug.png"))
    canny_pil.save(os.path.join(OUTPUT_DIR, "canny_debug.png"))

    STYLE_PROMPTS = {
    "realistic": "highly detailed realistic photograph, natural lighting, sharp focus, cinematic composition",

    "anime": "anime illustration, vibrant colors, clean line art, studio ghibli style shading, expressive lighting",

    "cartoon": "3d cartoon render, pixar style, soft global illumination, smooth textures, stylized proportions",

    "sketch": "pencil drawing, graphite shading, hand drawn illustration, paper texture, monochrome art"
       }

    base_prompt= STYLE_PROMPTS.get(style.lower(), "high quality digital art")

    prompt = f"{base_prompt},masterpiece" 

    result= pipe(prompt,
                negative_prompt="blurry, distorted, low quality, monochrome, messy",
                image=color_pil,
                control_image=[scribble_pil, canny_pil],
                strength=0.95,
                num_inference_steps=30,
                controlnet_conditioning_scale=[1,1.5],
                height=512,
                width=512,
                guidance_scale=8.5
                )
    
    image = result.images[0]

    #Save generated image
    filename= f"gen_{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)


    image.save(filepath)

    return{
        "image":f"http://127.0.0.1:8001/outputs/{filename}"
    }


