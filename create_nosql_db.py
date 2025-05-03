# create_db.py
# Script per creare e popolare MongoDB con file JSON

import os
import json
# pip install pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

def create_database():
    # 1. Connessione a MongoDB

    # client = MongoClient('mongodb://localhost:27017/')
    client = MongoClient("mongodb://root:example@localhost:27018/")

    db = client['dipa']
    collection = db['annotations_collection']

    # 2. Directory contenente i file JSON
    # directory = r'/home/fabio/Immagini/DIPA/annotations/CrowdWorks/labels'
    directory = "C:/Users/fabio/Pictures/DIPA/annotations/CrowdWorks/labels"

    # 3. Creazione indice unico su 'file_name'
    collection.create_index('file_name', unique=True)

    # 4. Lettura e inserimento dei file JSON
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    data['file_name'] = filename  # Aggiunge il nome del file al documento
                    collection.insert_one(data)
                    print(f"Inserito: {filename}")
            except DuplicateKeyError:
                print(f"Documento già presente: {filename}")
            except json.JSONDecodeError as e:
                print(f"Errore nel parsing JSON di {filename}: {e}")
            except Exception as e:
                print(f"Errore con il file {filename}: {e}")

    print("\n✅ Creazione e popolamento del database completati!")

if __name__ == "__main__":
    create_database()
