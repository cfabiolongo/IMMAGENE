import time
from actions import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars("X", "Y", "D", "H", "Z", "L", "M", "A", "D", "W")

# Image description reactor
class DESCR(Reactor): pass


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------

class main(Agent):
    def main(self):

        # World initialization
        init() >> [show_line("\nInitialiting agent...\n")]

        # Importing related triples
        load() >> [show_line("\nAsserting all OWL 2 triples beliefs...\n"), formulate_goal()]
        +DESCR(X) >> [show_line("\nImage description achieved: ", X), formulate_goal(X)]
        +GOAL(X, Y) >> [show_line("\nPlan formulation for the goal ",Y ," from the scenario ", X), formulate_plan(X)]


main().start()

# PHIDIAS.achieve(load(), "main")
