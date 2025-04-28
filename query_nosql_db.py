# query_db.py
import json
# pip install pymongo
from pymongo import MongoClient

def query_database(file_to_search):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['dipa']
    collection = db['annotations_collection']

    # result = collection.find_one({'file_name': file_to_search})

    # Estrai solo la prima parte del nome del file prima dell'underscore
    file_prefix = file_to_search.split('_')[0]

    # Esegui la ricerca usando la prima parte del nome
    result = collection.find_one({'file_name': {'$regex': f'^{file_prefix}'}})

    if result:
        print(f"\n📄 Documento trovato per {file_to_search}:\n")
        # --- SOLUZIONE: togliere _id prima di stampare
        result.pop('_id', None)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # Estrai defaultAnnotation
        default_annotation = result.get('defaultAnnotation', {})

        if not default_annotation:
            print("⚠️ Nessun campo 'defaultAnnotation' trovato nel documento.")
            return

        # Cicla sui sottocampi di defaultAnnotation
        for category_name, category_data in default_annotation.items():
            if_no_privacy = category_data.get('ifNoPrivacy', None)
            print(f"🧩 Categoria: {category_name} | ifNoPrivacy: {if_no_privacy}")

    else:
        print(f"\n❌ Nessun documento trovato per {file_to_search}")

if __name__ == "__main__":
    file_to_search = input("Inserisci il nome del file JSON da cercare (es: esempio.json): ").strip()
    if file_to_search:
        query_database(file_to_search)
    else:
        print("⚠️ Devi inserire un nome di file valido!")
