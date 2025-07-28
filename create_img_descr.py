import os
import pandas as pd
from tqdm import tqdm
from ollama_inference import describe_image

# Cartella contenente le immagini

prompt = "Describe very briefly."

# target dataset
# image_folder = "DIPA/images"
# output_excel = 'image_descriptions_t0_34b_dipa.xlsx'

# test dataset
image_folder = "DIPA_TEST"
output_excel = 'validation/inferences/image_descriptions_llama32_dipa-like.xlsx'

# model = llava:34b-v1.6-fp16, qwen2.5vl:72b, llama3.2-vision:90b-instruct-fp16, gemma3:27b-it-qat
model = "llama3.2-vision:90b-instruct-fp16"

# OLLAMA_API_URL_MULTI = "http://localhost:11434/api/generate"
OLLAMA_API_URL_MULTI = "http://172.16.61.73:11434/api/generate"
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

print(f"File saved: {output_excel}")
