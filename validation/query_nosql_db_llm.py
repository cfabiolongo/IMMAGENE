import pandas as pd  # aggiunto per leggere il file Excel
from pymongo import MongoClient

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ollama_inference import ask_ollama_stream


# home (localhost):
# llama3:8b-instruct-q8_0, qwen2.5:14b-instruct-q6_K, mistral:7b-instruct-q8_0

# work (172.16.61.73):
# server: llama3.3:70b-instruct-fp16, qwen2.5:72b-instruct-fp16, llama4:17b-scout-16e-instruct-q8_0
# local: qwen2.5:14b-instruct-q8_0

OLLAMA_API_URL = "http://172.16.61.73:11434/api/generate"
# OLLAMA_API_URL = "http://localhost:11434/api/generate"

text_model = "qwen2.5:72b-instruct-fp16"
temp = 0.8

# Inizializza una lista per salvare le risposte
file_input = []
file_dipa = []
response = []
ground_truth_number = []
extracted_features = []
explanation = []
description = []


def query_database(file_to_search, ref_dipa, prompt):

    # with credentials
    #client = MongoClient("mongodb://root:example@localhost:27017/")

    # without credentials
    client = MongoClient('mongodb://localhost:27017/')

    db = client['dipa']
    collection = db['annotations_collection']

    file_prefix = file_to_search.split('_')[0]
    result = collection.find_one({'file_name': {'$regex': f'^{file_prefix}'}})

    if result:
        print(f"\n📄 Documento trovato per {file_to_search}:\n")
        result.pop('_id', None)
        # print(json.dumps(result, indent=2, ensure_ascii=False))

        default_annotation = result.get('defaultAnnotation', {})

        if not default_annotation:
            print("⚠️ Nessun campo 'defaultAnnotation' trovato nel documento.")
            return

        no_privacy_false_categories = []

        for category_name, category_data in default_annotation.items():
            if_no_privacy = category_data.get('ifNoPrivacy', None)
            print(f"🧩 Categoria: {category_name} | ifNoPrivacy: {if_no_privacy}")

            if if_no_privacy is False:
                no_privacy_false_categories.append(category_name)

        print("\nCategorie con ifNoPrivacy == False:")
        print(no_privacy_false_categories)

        # system_prompt = f"In the following description, answer with a single boolean TRUE or FALSE, weather or not you found items (or similar) from the following privacy-threating list: {no_privacy_false_categories}. The boolean must be followed by the number of found items (e.g TRUE 2). Report also which items you found."

        # zero-shot
        system_prompt = f"In the following description, answer with a single boolean TRUE or FALSE, weather or not you found privacy-threating items. The boolean must be followed by the number of found items (e.g TRUE 2). Report also what items you found."

        meta_outcome = ask_ollama_stream(OLLAMA_API_URL, prompt, system_prompt, temp, text_model)
        # print(f"meta-outcome: {meta_outcome}")

        # solo per modelli chain-of-thoughs
        # meta_outcome = re.sub(r"<think>.*?</think>", "",  meta_outcome, flags=re.DOTALL)

        print(f"\nmeta-outcome senza cot: {meta_outcome}")

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

        file_input.append(file_to_search)
        file_dipa.append(ref_dipa)
        response.append(part1)
        ground_truth_number.append(len(no_privacy_false_categories))
        extracted_features.append(part2)
        explanation.append(meta_outcome)
        description.append(prompt)

    else:
        print(f"\n❌ Nessun documento trovato per {file_to_search}")

if __name__ == "__main__":

    # Carica il file Excel
    excel_path = "inferences/risultati_validazione_qwen_test800.xlsx"
    df_result = pd.read_excel(excel_path)

    # Controlla che la colonna esista
    if "matched_file_image_name" not in df_result.columns or "input_description" not in df_result.columns:
        print("❌ Colonne richieste non trovate nel file Excel.")
    else:
        # Itera sulle righe del DataFrame
        for _, row in df_result.iterrows():
            reference = str(row["input_file_image_name"]).strip()
            descr = row["input_description"]
            print(f"\n>>>>> Closer item to {reference} whose description is: {descr}")
            file_name = str(row["matched_file_image_name"]).strip()

            if pd.notna(file_name) and file_name:
                query_database(file_name.split('.')[0], reference, descr)

        # Creazione del DataFrame
        output_df = pd.DataFrame({
            'file_input': file_input,
            'reference': file_dipa,
            'response': response,
            'ground_truth_ft_number': ground_truth_number,
            'extracted_features': extracted_features,
            'explanation': explanation,
            'description': description
        })

        output_path = "inferences/meta_zero-shot_overall_qwen_llama.xlsx"
        output_df.to_excel(output_path, index=False)
        print(f"\n✅ File Excel salvato in: {output_path}")
