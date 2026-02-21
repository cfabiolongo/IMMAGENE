import sys
import os
import queue
from pymongo import MongoClient
from ollama_inference import ask_ollama_stream, describe_image_status
import time
import sqlite3
import numpy as np
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer
# pip install huggingface_hub[hf_xet]
from sklearn.metrics.pairwise import cosine_similarity


from phidias.Lib import *
from phidias.Agent import *
from phidias.Types import *

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# DB Section
NOSQL_CONN = config.get('DATABASE', 'NOSQL_CONN')
NOSQL_DB = config.get('DATABASE', 'NOSQL_DB')
NOSQL_COLLECTION = config.get('DATABASE', 'NOSQL_COLLECTION')
VECT_DB = config.get('DATABASE', 'VECT_DB')

client = MongoClient(NOSQL_CONN)
db = client[NOSQL_DB]
collection = db[NOSQL_COLLECTION]

# Local path to save the embedding model
MODEL_DIR = "./all-MiniLM-L6-v2"

def load_or_download_model(model_dir):
    if os.path.isdir(model_dir) and os.path.exists(os.path.join(model_dir, 'config.json')):
        print(f"✅ Modello trovato localmente in: {model_dir}")
        model = SentenceTransformer(model_dir)
    else:
        print(f"⬇️  Modello non trovato, scarico da Hugging Face e salvo in: {model_dir}")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        model.save(model_dir)
        print("💾 Modello salvato localmente.")
    return model

# loading model
model = load_or_download_model(MODEL_DIR)

sys.path.insert(0, "../lib")


# LLM Multi-Modal Section
MM_HOST = config.get('MULTI_LLM', 'HOST')
MM_MODEL = config.get('MULTI_LLM', 'MODEL')
MM_TEMP = config.get('MULTI_LLM', 'TEMP')
MM_SYSTEM = config.get('MULTI_LLM', 'SYSTEM')

# LLM text Section
HOST = config.get('TEXT_LLM', 'HOST')
MODEL = config.get('TEXT_LLM', 'MODEL')
TEMP = config.get('TEXT_LLM', 'TEMP')
SYSTEM = config.get('TEXT_LLM', 'SYSTEM')

# Testing inference Section
IMAGES_PATH = config.get('INFERENCE', 'IMAGES_PATH')
IMAGES = config.get('INFERENCE', 'IMAGES_LIST')



# Agent classes
class init(Procedure): pass

class setup(Procedure): pass

class DESCR(Reactor): pass

class PLAN(Reactor): pass

class GOAL(Reactor): pass

class ACTUATION(Reactor): pass



class actuate_plan(Action):
    """Formulate goal from image description"""
    def execute(self, arg1, arg2):
        plan = str(arg1).split("'")[3]
        act = str(arg2).split("'")[3]
        print(f"\nActuating plan: {plan} with {act}.")



class formulate_goal(Action):
    """Formulate goal from image description"""
    def execute(self, arg):
        # print(f"arg1: {arg}")
        descr = str(arg).split("'")[3]
        # print(f"descr: {descr}")

        print("Formulating goal...")
        goal = "[FORMULATED_GOAL]"
        self.assert_belief(GOAL(descr, goal))


class formulate_plan(Action):
    """create sparql query from MST"""
    def execute(self, arg1, arg2):

        # print(f"arg1: {arg1}")
        # print(f"arg2: {arg2}")

        descr = str(arg1).split("'")[3]
        goal = str(arg2).split("'")[3]

        print("Formulating plan...")
        plan = "[FORMULATED_PLAN]"
        self.assert_belief(PLAN(descr, goal, plan))


class formulate_action(Action):

    """create sparql query from MST"""
    def execute(self, arg1, arg2, arg3):

        # print(f"arg1: {arg1}")
        # print(f"arg2: {arg2}")
        # print(f"arg3: {arg3}")

        descr = str(arg1).split("'")[3]
        goal = str(arg2).split("'")[3]
        plan = str(arg3).split("'")[3]

        print("Formulating action...")
        action = "[FORMULATED_ACTION]"
        self.assert_belief(ACTUATION(descr, goal, plan, action))



class ack_plan(ActiveBelief):
    """ActiveBelief for achieving acknowledgement from LLM for the current plan"""
    def evaluate(self, arg1, arg2):

        descr = str(arg1).split("'")[3]
        plan = str(arg2).split("'")[3]

        print(f"\nPlan {plan} assessment for the scenario {descr}...")

        start_time = time.time()
        result = find_most_similar(descr)
        elapsed_time = time.time() - start_time

        print(f"\n🔍 Closer result: {result}")
        print(f"Vector db retrieval time: {elapsed_time}")

        file_to_search = result['file_image_name'].split(".")[0]
        privacy_threatening_list = query_database(file_to_search)
        print(f"\nPrivacy threatening items: {privacy_threatening_list}")

        list_str = ", ".join(privacy_threatening_list)
        SYSTEM_PROMPT = SYSTEM.replace("[LIST]", list_str)

        meta_start_time = time.time()
        meta_outcome = ask_ollama_stream(HOST, descr, SYSTEM_PROMPT, TEMP, MODEL)
        meta_elapsed_time = time.time() - meta_start_time

        # only for chain-of-thoughs models (e.g. deedseek, qwen)
        # meta_outcome = re.sub(r"<think>.*?</think>", "",  meta_outcome, flags=re.DOTALL)

        #print(f"\nmeta-assessment: {meta_outcome}")

        meta_outcome = meta_outcome.replace("\n", " ")

        parti = meta_outcome.split(" ")

        # Fill the list with empty strings if it has less than 3 elements
        while len(parti) < 3:
            parti.append("")

        response = parti[0].strip()
        features = parti[1].strip()
        expl = ' '.join(parti[2:])
        meta_elapsed_time = time.time() - start_time
        print(f"Meta inference time: {meta_elapsed_time}")

        print(f"- Response: {response}")
        print(f"- #Features found: {features}")
        print(f"- Explanation: {expl}")

        if response == "TRUE":
            return False
        else:
            return True


################ Meta-Reasoning Section ################


class achieve_img_descr(Action):
    """Formulate goal from image description"""
    def execute(self):

        image_path = IMAGES_PATH+"/"+IMAGES
        print(f"Img path: {image_path}")

        success, descr, inference_time = describe_image_status(MM_HOST, image_path, MM_SYSTEM, MM_TEMP, MM_MODEL)

        if success:
            print(f"Img descr: {descr}")
            print(f"visual inference time: {inference_time}")
            self.assert_belief(DESCR(descr))
        else:
            print(descr)


def find_most_similar(input_text):
    input_embedding = model.encode(input_text).astype(np.float32)

    conn = sqlite3.connect(VECT_DB)
    c = conn.cursor()
    c.execute('SELECT id, file_image_name, description, embedding FROM immagini')
    rows = c.fetchall()
    conn.close()

    best_score = -1
    best_row = None

    for row in rows:
        row_id, file_name, desc, emb_blob = row
        emb_array = np.frombuffer(emb_blob, dtype=np.float32)
        score = cosine_similarity([input_embedding], [emb_array])[0][0]
        if score > best_score:
            best_score = score
            best_row = {
                "id": row_id,
                "file_image_name": file_name,
                "description": desc,
                "similarity": round(score, 4)
            }

    return best_row



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


