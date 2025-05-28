import time
from actions_mas import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars("D", "G",  "P", "A", "X")

# ---------------------------------------------------------------------
# Agents section
# ---------------------------------------------------------------------

def create_agent(class_name):
    def main(self):
        # Custom intention
        +DESCR(D, P)[{'from': A}] / ack_plan(D, P) >> [-DESCR(D, P), show_line("\nReceived belief DESCR(",D,") from ", A), accept()]
        +DESCR(D, P)[{'from': A}] >> [-DESCR(D, P), show_line("\nReceived belief DESCR(",D,") from ", A), refuse()]

        accept() >> [show_line("\n>>>>>>>> Accepting plan\n"), +ACK("TRUE")[{'to': 'main'}]]
        refuse() >> [show_line("\n>>>>>>>> Refusing plan\n"), +ACK("FALSE")[{'to': 'main'}]]

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

        init() >> [show_line("\nAchieving img description. Waiting...\n"), achieve_img_descr(), setup()]

        setup() / DESCR(D) >> [show_line("\nImage description achieved: ", D), formulate_goal(D), achieve_plan()]

        achieve_plan() / (DESCR(D) & GOAL(G)) >> [show_line("\nPlanning for the goal: ", G, " from the description ", D), formulate_plan(D, G), commit()]

        commit() / (DESCR(D) & GOAL(G) & PLAN(P)) >> [+DESCR(D, P)[{'to': "metaval"}], show_line("\n>>>>>>>> Communication started <<<<<<<<<\n")]

        +ACK(X)[{'from': A}] >> [show_line(">>>>>>>> received ackowledgemt ",X," from ", A)]


        #+PLAN(D, G, P) >> [show_line("\nActions implementation the plan ", P, " to achieve the goal ", G, " from the scenario ", D), formulate_action(D, G, P)]
        #+ACTION(D, G, P, A) / ack_plan(D, P) >> [show_line("\nCommitting the action ", A, " implementing the plan ", P, ".")]

main().start()

# PHIDIAS.achieve(init(), "main")