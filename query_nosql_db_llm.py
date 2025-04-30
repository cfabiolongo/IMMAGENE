# query_db.py
import json
import pandas as pd  # aggiunto per leggere il file Excel
from pymongo import MongoClient
from ollama_inference import ask_ollama_stream

# home:
# llama3:8b-instruct-q8_0, qwen2.5:14b-instruct-q6_K

# work:
# llama3.3:70b-instruct-fp16, qwen2.5:14b-instruct-q8_0

OLLAMA_API_URL = "http://172.16.61.73:11434/api/generate"
text_model = "llama3.3:70b-instruct-fp16"
temp = 0.8

# Inizializza una lista per salvare le risposte
responses = []
explanations = []



def query_database(file_to_search, prompt):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['dipa']
    collection = db['annotations_collection']

    file_prefix = file_to_search.split('_')[0]
    result = collection.find_one({'file_name': {'$regex': f'^{file_prefix}'}})

    if result:
        print(f"\n📄 Documento trovato per {file_to_search}:\n")
        result.pop('_id', None)
        print(json.dumps(result, indent=2, ensure_ascii=False))

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

        system_prompt = f"In the following description, answer with TRUE or FALSE if there are elements of the following privacy-threating list: {no_privacy_false_categories}. Then, also tell me which elements you found."

        meta_outcome = ask_ollama_stream(OLLAMA_API_URL, prompt, system_prompt, temp, text_model)
        responses.append(meta_outcome)
        print(meta_outcome)

    else:
        print(f"\n❌ Nessun documento trovato per {file_to_search}")

if __name__ == "__main__":
    import pandas as pd

    # Carica il file Excel
    excel_path = "mismatch_risultati_test300.xlsx"
    df = pd.read_excel(excel_path)

    # Controlla che la colonna esista
    if "matched_file_image_name" not in df.columns or "input_description" not in df.columns:
        print("❌ Colonne richieste non trovate nel file Excel.")
    else:
        # Itera sulle righe del DataFrame
        for _, row in df.iterrows():
            reference = str(row["input_file_image_name"]).strip()
            print(f"\n>>>>> Closer item to {reference}: ")
            file_name = str(row["matched_file_image_name"]).strip()
            descr = row["input_description"]

            if pd.notna(file_name) and file_name:
                query_database(file_name.split('.')[0], descr)

# system: In the following description, answer with TRUE or FALSE if there are elements of the following privacy-threating list:
# ['Human hair', 'Building', 'Person', 'Boy', 'Man']. Then, also tell me which elements you found.