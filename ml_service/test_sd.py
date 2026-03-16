from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)

pipe = pipe.to("cpu")

image = pipe("a simple pencil sketch of a cat").images[0]

image.save("test_output.png")

print("Generated image saved.")