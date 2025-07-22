import os
import pandas as pd
from tqdm import tqdm
from ollama_inference import describe_image
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['dipa']
collection = db['annotations_collection']

def query_database(file_to_search):

    file_prefix = file_to_search.split('_')[0]
    result = collection.find_one({'file_name': {'$regex': f'^{file_prefix}'}})
    no_privacy_false_categories = []

    if result:
        print(f"\n📄 Document found for {file_to_search}:\n")
        result.pop('_id', None)

        default_annotation = result.get('defaultAnnotation', {})

        if not default_annotation:
            print("⚠️ No field 'defaultAnnotation' found in the document.")
            return

        for category_name, category_data in default_annotation.items():
            if_no_privacy = category_data.get('ifNoPrivacy', None)
            print(f"🧩 Categoria: {category_name} | ifNoPrivacy: {if_no_privacy}")

            if if_no_privacy is False:
                no_privacy_false_categories.append(category_name)
    else:
        print(f"\n❌ No documents found for {file_to_search}")

    return no_privacy_false_categories


dipa_cat = ['Person','Place Identifier','Identity','Home','Interior','Vehicle Plate','Bystander','Food','Printed Materials','Screen','Clothing','Scenery','Pet','Book','Photo','Machine','Table','Electronic Devices','Cosmetics','Toy','Finger','Cigarettes','Accident','Musical Instrument','Nudity','Accessory']


# Dataset non-guided prompt
#prompt = "Answer with TRUE if you find privacy-threating items in the image, otherwise answer FALSE. The response must be followed by the number of found items (e.g TRUE 2). Report also which items you found."

# Dataset guided prompt (with categories)
prompt = f"Answer with TRUE if you find privacy-threating items in the image from the following list: {dipa_cat}, otherwise answer FALSE. The response must be followed by the number of found items (e.g TRUE 2). Report also which items you found."
print(prompt)

# test dataset
image_folder = "../DIPA_TEST"
output_excel = 'direct_image_descr_gemma3-27b-90b_dipa_guided.xlsx'

# model = llava:34b-v1.6-fp16, llama3.2-vision:11b-instruct-q8_0, qwen2.5vl:72b, llama3.2-vision:90b-instruct-fp16, gemma3:27b-it-qat
model = "gemma3:27b-it-qat"

# OLLAMA_API_URL_MULTI = "http://localhost:11434/api/generate"
OLLAMA_API_URL_MULTI = "http://172.16.61.73:11434/api/generate"
temp = 0.8

# Estensioni valide per le immagini
valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

# Ottenere la lista dei file immagine
image_files = [f for f in os.listdir(image_folder)
               if os.path.splitext(f)[1].lower() in valid_extensions]

# Inizializza una lista per salvare le risposte
file_dipa = []
response = []
ground_truth_ft_number = []
explanation = []
description = []
extracted_features = []
ground_truth_response = []

# Elaborazione con barra di progresso
for filename in tqdm(image_files, desc="Inferenza immagini"):
    image_path = os.path.join(image_folder, filename)

    meta_outcome = describe_image(OLLAMA_API_URL_MULTI, image_path, prompt, temp, model)

    print(f"\nmeta-evaluation: {meta_outcome}")

    meta_outcome = meta_outcome.replace("\n", " ")

    parti = meta_outcome.split(" ")

    # Completa la lista con stringhe vuote se ha meno di 3 elementi
    while len(parti) < 3:
        parti.append("")

    part1 = parti[0].strip()
    part2 = parti[1].strip()

    print(f"response: {part1}")
    print(f"ft: {part2}")
    print(f"expl: {meta_outcome}")

    file_to_search = filename.split(".")[0]
    privacy_threatening_list = query_database(file_to_search)
    print(f"\nPrivacy threatening items: {privacy_threatening_list}")
    print(f"Privacy threatening assessment: {len(privacy_threatening_list)>0}")
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

    file_dipa.append(filename)
    response.append(part1)
    extracted_features.append(part2)
    explanation.append(meta_outcome)
    ground_truth_ft_number.append(len(privacy_threatening_list))
    if len(privacy_threatening_list) > 0:
        ground_truth_response.append("TRUE")
    else:
        ground_truth_response.append("FALSE")



# Creazione del DataFrame
df = pd.DataFrame({
    'reference': file_dipa,
    'response': response,
    'extracted_features': extracted_features,
    'explanation': explanation,
    'ground_truth_ft_number': ground_truth_ft_number,
    'ground_truth_response': ground_truth_response
})

output_df = pd.DataFrame(df)
output_df.to_excel(output_excel, index=False)
print(f"\n✅ File Excel salvato in: {output_excel}")