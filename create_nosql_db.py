# create_db.py
# Script to create and popolate MongoDB with JSON files

import os
import json
# pip install pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

def create_database():

    # 1. Connecting to MongoDB
    # client = MongoClient('mongodb://localhost:27017/')
    client = MongoClient("mongodb://root:example@localhost:27018/")

    db = client['dipa']
    collection = db['annotations_collection']

    # 2. Directory containing JSON files
    # directory = r'/home/fabio/Immagini/DIPA/annotations/CrowdWorks/labels'
    directory = "C:/Users/fabio/Pictures/DIPA/annotations/CrowdWorks/labels"

    # 3. Unique index Creation on 'file_name'
    collection.create_index('file_name', unique=True)

    # 4. Readind and inserting JSON files
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
                print(f"Documento already existing: {filename}")
            except json.JSONDecodeError as e:
                print(f"Error JSON parsing JSON of {filename}: {e}")
            except Exception as e:
                print(f"Error with the file {filename}: {e}")

    print("\n✅ Database creation and population completed!")

if __name__ == "__main__":
    create_database()
