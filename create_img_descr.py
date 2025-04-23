import os
import subprocess
import pandas as pd
from tqdm import tqdm
import json

# Cartella contenente le immagini
image_folder = "C:/Users/fabio/Pictures/DIPA/images"
prompt_instruction = "Provide a brief list of subjects and actions from the picture, with no further text."
output_excel = 'image_descriptions_noq.xlsx'

ollama_host = "http://localhost:11434"
model = "llava:13b-v1.5-q6_K"

# ollama_host = "http://172.16.61.73:11434"
# model = "llava:34b-v1.6-fp16"




# Estensioni valide per le immagini
valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

# Ottenere la lista dei file immagine
image_files = [f for f in os.listdir(image_folder)
               if os.path.splitext(f)[1].lower() in valid_extensions]

results = []

# Elaborazione con barra di progresso
for filename in tqdm(image_files, desc="Inferenza immagini"):
    image_path = os.path.join(image_folder, filename)

    prompt_data = {
        "prompt": f"<image>\n{prompt_instruction}",
        "temperature": 0.0
    }

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=json.dumps(prompt_data),
            text=True,
            capture_output=True,
            check=True,
            env={
                **os.environ,
                "OLLAMA_HOST": ollama_host,
                "OLLAMA_IMAGE": image_path
            },
            encoding='utf-8'
        )
        description = result.stdout.strip() if result.stdout else "No output"
        print(description)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Errore sconosciuto"
        description = f"Errore: {error_msg}"

    results.append({
        'file_image_name': filename,
        'description': description
    })


# Creare un DataFrame e salvare in un file Excel
df = pd.DataFrame(results)
df.to_excel(output_excel, index=False)

print(f"File salvato: {output_excel}")
