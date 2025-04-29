import os
import pandas as pd
from diffusers import DiffusionPipeline
import torch
from huggingface_hub import login
from tqdm import tqdm  # Barra di progresso

# Login Hugging Face
login(token="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")

# Percorso del modello
model_path = "/stlab/models/stable-diffusion-3.5-large"

# Carica pipeline
pipe = DiffusionPipeline.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
).to("cuda:3")

# Crea cartella di output se non esiste
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# Carica file Excel
df = pd.read_excel("image_descriptions_t08_34b_plus_actions_70b.xlsx")

# Itera con barra di progresso
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Generazione immagini"):
    prompt = row["description"]
    filename = row["file_image_name"]
    output_name = os.path.splitext(filename)[0] + "_diff.jpg"
    output_path = os.path.join(output_dir, output_name)

    # Salta se l'immagine è già stata generata
    if os.path.exists(output_path):
        continue

    try:
        image = pipe(prompt).images[0]
        image.save(output_path)
    except Exception as e:
        print(f"[Errore] Riga {idx} - '{filename}': {e}")
