# query_db.py
import json
# pip install pymongo
from pymongo import MongoClient

def query_database(file_to_search):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['dipa']
    collection = db['annotations_collection']

    result = collection.find_one({'file_name': file_to_search})

    if result:
        print(f"\n📄 Documento trovato per {file_to_search}:\n")
        # --- SOLUZIONE: togliere _id prima di stampare
        result.pop('_id', None)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n❌ Nessun documento trovato per {file_to_search}")

if __name__ == "__main__":
    file_to_search = input("Inserisci il nome del file JSON da cercare (es: esempio.json): ").strip()
    if file_to_search:
        query_database(file_to_search)
    else:
        print("⚠️ Devi inserire un nome di file valido!")
