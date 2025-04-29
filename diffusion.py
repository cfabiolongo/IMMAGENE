import os
from diffusers import DiffusionPipeline

from huggingface_hub import login
login(token="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")

model_path = "/home/fabio/TEMP/stable-diffusion-3.5-large"

pipe = DiffusionPipeline.from_pretrained(model_path)

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = pipe(prompt).images[0]

# Se vuoi salvare l'immagine:
image.save("output.png")

