import time
from actions import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars("D", "G",  "P", "A", "X")

class DESCR(Belief): pass

class ACK(Reactor): pass

class commit(Procedure): pass


# ---------------------------------------------------------------------
# Agents section
# ---------------------------------------------------------------------

def create_agent(class_name):
    def main(self):
        # Custom intention
        +DESCR(X)[{'from': A}] >> [-DESCR(X), show_line("\nReceived belief DESCR(",X,") from ", A), +ACK("TRUE")[{'to': 'main'}]]

    return type(class_name, (Agent,), {"main": main})


# custom agent rocco
globals()["metaval"] = create_agent("metaval")
instance = globals()["metaval"]()


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------


# Custom agent
instance = globals()["metaval"]()
instance.start()


class main(Agent):
    def main(self):

        init() >> [show_line("\nAchieving img description. Waiting...\n"), achieve_img_descr()]

        +DESCR(D) >> [+DESCR(D)[{'to': "metaval"}], show_line("\nImage description achieved: ", D), formulate_goal(D)]

        +ACK(X)[{'from': A}] >> [show_line(">>>>>>>> received ackowledgemt from ", A)]

        #+GOAL(D, G) >> [show_line("\nPlanning for the goal: ", G, " from the description ", D), formulate_plan(D, G)]
        #+PLAN(D, G, P) >> [show_line("\nActions implementation the plan ", P, " to achieve the goal ", G, " from the scenario ", D), formulate_action(D, G, P)]
        #+ACTION(D, G, P, A) / ack_plan(D, P) >> [show_line("\nCommitting the action ", A, " implementing the plan ", P, ".")]

main().start()

# PHIDIAS.achieve(init(), "main")