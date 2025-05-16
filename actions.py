import sys
import queue

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



# ---------------------------------------------------------------------
# Non-ontological rendering variables
# ---------------------------------------------------------------------




# ---------------------------------------------------------------------
# System procedures section
# ---------------------------------------------------------------------


# Ontology intialization
class init(Procedure): pass
# Import OWL triples

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