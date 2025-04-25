import os
import subprocess
import pandas as pd
from tqdm import tqdm
import json
from ollama_inference import ask_ollama_stream, describe_image

# Cartella contenente le immagini
image_folder = "C:/Users/fabio/Pictures/DIPA/images"
prompt = "Provide a detailed list of subjects and actions from the picture, with no further text."
output_excel = 'image_descriptions_t0_34b.xlsx'

ollama_host = "http://localhost:11434"
model = "llava:13b-v1.5-q6_K"

#ollama_host = "http://172.16.61.73:11434"
#model = "llava:34b-v1.6-fp16"


OLLAMA_API_URL_MULTI = "http://localhost:11434/api/generate"
temp = 0.8

# Estensioni valide per le immagini
valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

# Ottenere la lista dei file immagine
image_files = [f for f in os.listdir(image_folder)
               if os.path.splitext(f)[1].lower() in valid_extensions]

results = []

# Elaborazione con barra di progresso
for filename in tqdm(image_files, desc="Inferenza immagini"):
    image_path = os.path.join(image_folder, filename)

    description = describe_image(OLLAMA_API_URL_MULTI, image_path, prompt, temp, model)
    print(f"{filename} --> {description}")

    results.append({
        'file_image_name': filename,
        'description': description
    })


# Creare un DataFrame e salvare in un file Excel
df = pd.DataFrame(results)
df.to_excel(output_excel, index=False)

print(f"File salvato: {output_excel}")
