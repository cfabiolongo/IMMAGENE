from diffusers import DiffusionPipeline
import torch
from huggingface_hub import login

login(token="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")

model_path = "/stlab/models/stable-diffusion-3.5-large"

pipe = DiffusionPipeline.from_pretrained(
    model_path,
    torch_dtype=torch.float16,  # Usa float16 per maggiore velocità e minor consumo di memoria
).to("cuda")  # Sposta il modello sulla GPU

prompt = "There are several plants hanging from the upper parts of the facade, adding greenery to the urban setting. In front of the pub, there is outdoor seating consisting of tables with chairs. The area appears to be pedestrian-friendly, with no visible traffic or vehicles in the immediate vicinity. A clear blue sky suggests it might be a sunny day."

image = pipe(prompt).images[0]

image.save("output2.png")

