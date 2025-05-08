import sys
import random
import turtle
import tkinter as tk
from tkinter import messagebox
import threading
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
config.read('config_dtwin.ini')

# ONTOLOGY section
FILE_NAME = config.get('ONTOLOGY', 'FILE_NAME')
ONTO_NAME = config.get('ONTOLOGY', 'ONTO_NAME')

# REASONING Section
REASONING_ACTIVE = config.getboolean('REASONING', 'ACTIVE')
REASONER = config.get('REASONING', 'REASONER').split(",")
PREFIXES = config.get('REASONING', 'PREFIXES').split(",")
PREFIX = " ".join(PREFIXES)
PREFIX = PREFIX + f"PREFIX {ONTO_NAME}: <http://test.org/{FILE_NAME}#> "

# BDI-CLASSES Section
ENTITIES = config.get('CLASSES', 'Entities').split(",")

# Properties
BELIEFS = config.get('CLASSES', 'PHI-Beliefs').split(",")
REACTORS = config.get('CLASSES', 'PHI-Reactors').split(",")
DESIRES = config.get('CLASSES', 'PHI-Desires').split(",")
INTENTIONS = config.get('CLASSES', 'PHI-Intentions').split(",")

PROPERTIES = config.get('CLASSES', 'Properties').split(",")
DATAS = config.get('CLASSES', 'Data').split(",")


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
    """create sparql query from MST"""
    def execute(self, arg):
        print(f"arg1: {arg}")

        print("Formulating goal...")
        goal = "Formulated goal"
        self.assert_belief(GOAL(goal))


class formulate_plan(Action):
    """create sparql query from MST"""
    def execute(self, arg1, arg2):

        print(f"arg1: {arg1}")
        print(f"arg2: {arg2}")

        print("Formulating plan...")
        plan = "Formulated plan"
        self.assert_belief(GOAL(plan))


class formulate_action(Action):

    """create sparql query from MST"""
    def execute(self, arg1, arg2, arg3):

        print(f"arg1: {arg1}")
        print(f"arg2: {arg2}")
        print(f"arg3: {arg3}")

        print("Formulating goal...")
        goal = "Formulated goal"
        self.assert_belief(GOAL(goal))



class ack_plan(ActiveBelief):
    """ActiveBelief for achieving acknowledgement from LLM on the current plan"""
    def evaluate(self, arg1, arg2):

        print(f"arg1: {arg1}")
        print(f"arg2: {arg2}")

        # description = str(arg1).split("'")[3]
        # plan = str(arg2).split("'")[1]

        return True