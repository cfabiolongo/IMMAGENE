# query_db.py
import json
# pip install pymongo
from pymongo import MongoClient

def query_database(file_to_search):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['dipa']
    collection = db['annotations_collection']

    file_prefix = file_to_search.split('_')[0]
    result = collection.find_one({'file_name': {'$regex': f'^{file_prefix}'}})

    if result:
        print(f"\n📄 Document found for {file_to_search}:\n")
        result.pop('_id', None)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        default_annotation = result.get('defaultAnnotation', {})

        if not default_annotation:
            print("⚠️ No field 'defaultAnnotation' found in the document.")
            return

        no_privacy_false_categories = []

        for category_name, category_data in default_annotation.items():
            if_no_privacy = category_data.get('ifNoPrivacy', None)
            print(f"🧩 Categoria: {category_name} | ifNoPrivacy: {if_no_privacy}")

            if if_no_privacy is False:
                no_privacy_false_categories.append(category_name)

        print("\nCategorie con ifNoPrivacy == False:")
        print(no_privacy_false_categories)
    else:
        print(f"\n❌ No documents found for {file_to_search}")

if __name__ == "__main__":
    file_to_search = input("Insert the image file name (without extension) to be searched (e.g 00b4064b073e51f3): ").strip()
    if file_to_search:
        query_database(file_to_search)
    else:
        print("⚠️ Please insert a valid file name!")

