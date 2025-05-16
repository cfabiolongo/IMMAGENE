import sys
import queue
from pymongo import MongoClient
from ollama_inference import ask_ollama_stream, describe_image

# Coda per inviare richieste di query
query_queue = queue.Queue()

# Coda per restituire i risultati delle query
result_queue = queue.Queue()

sys.path.insert(0, "../lib")

from phidias.Lib import *
from phidias.Agent import *
from phidias.Types import *

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

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

class DESCR(Reactor): pass

class PLAN(Reactor): pass

class GOAL(Reactor): pass

class ACTION(Reactor): pass


class formulate_goal(Action):
    """Formulate goal from imahge description"""
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
        self.assert_belief(ACTION(descr, goal, plan, action))



class ack_plan(ActiveBelief):
    """ActiveBelief for achieving acknowledgement from LLM on the current plan"""
    def evaluate(self, arg1, arg2):

        # print(f"arg1: {arg1}")
        # print(f"arg2: {arg2}")

        descr = str(arg1).split("'")[3]
        plan = str(arg2).split("'")[3]

        print(f"\nPlan {plan} assessment for the scenario {descr}")

        return True


################ Meta-Reasoning Section ################




class achieve_img_descr(Action):
    """Formulate goal from imahge description"""
    def execute(self):

        image_path = IMAGES_PATH+"/"+IMAGES
        print(f"Img path: {image_path}")

        descr = describe_image(MM_HOST, image_path, MM_SYSTEM, MM_TEMP, MM_MODEL)

        print(f"Img descr: {descr}")
        self.assert_belief(DESCR(descr))



#
# def query_database(file_to_search, prompt):
#
#     # with credentials
#     #client = MongoClient("mongodb://root:example@localhost:27017/")
#
#     # without credentials
#     client = MongoClient('mongodb://localhost:27017/')
#
#     db = client['dipa']
#     collection = db['annotations_collection']
#
#     file_prefix = file_to_search.split('_')[0]
#     result = collection.find_one({'file_name': {'$regex': f'^{file_prefix}'}})
#
#     if result:
#         print(f"\n📄 Documento trovato per {file_to_search}:\n")
#         result.pop('_id', None)
#         # print(json.dumps(result, indent=2, ensure_ascii=False))
#
#         default_annotation = result.get('defaultAnnotation', {})
#
#         if not default_annotation:
#             print("⚠️ Nessun campo 'defaultAnnotation' trovato nel documento.")
#             return
#
#         no_privacy_false_categories = []
#
#         for category_name, category_data in default_annotation.items():
#             if_no_privacy = category_data.get('ifNoPrivacy', None)
#             print(f"🧩 Categoria: {category_name} | ifNoPrivacy: {if_no_privacy}")
#
#             if if_no_privacy is False:
#                 no_privacy_false_categories.append(category_name)
#
#         print("\nCategorie con ifNoPrivacy == False:")
#         print(no_privacy_false_categories)
#
#         system_prompt = f"In the following description, answer with a single boolean TRUE or FALSE, weather or not you found items (or similar) from the following privacy-threating list: {no_privacy_false_categories}. The boolean must be followed by the number of found items (e.g TRUE 2). Report also which items you found."
#
#         # zero-shot
#         # system_prompt = f"In the following description, answer with a single boolean TRUE or FALSE, weather or not you found privacy-threating items. The boolean must be followed by the number of found items (e.g TRUE 2). Report also which items you found."
#
#
#         meta_outcome = ask_ollama_stream(OLLAMA_API_URL, prompt, system_prompt, temp, text_model)
#         # print(f"meta-outcome: {meta_outcome}")
#
#         # solo per modelli chain-of-thoughs
#         # meta_outcome = re.sub(r"<think>.*?</think>", "",  meta_outcome, flags=re.DOTALL)
#
#         print(f"\nmeta-outcome senza cot: {meta_outcome}")
#
#         meta_outcome = meta_outcome.replace("\n", " ")
#
#         parti = meta_outcome.split(" ")
#
#         # Completa la lista con stringhe vuote se ha meno di 3 elementi
#         while len(parti) < 3:
#             parti.append("")
#
#         part1 = parti[0].strip()
#         part2 = parti[1].strip()
#
#         print(f"response: {part1}")
#         print(f"ft: {part2}")
#         print(f"expl: {meta_outcome}")
#
#         file_dipa.append(file_name)
#         response.append(part1)
#         ground_truth_number.append(len(no_privacy_false_categories))
#         extracted_features.append(part2)
#         explanation.append(meta_outcome)
#         description.append(prompt)
#
#     else:
#         print(f"\n❌ Nessun documento trovato per {file_to_search}")
