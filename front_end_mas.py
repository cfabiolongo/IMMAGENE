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
        # Related-Plan assessment
        +DESCR(D, P)[{'from': A}] / ack_plan(D, P) >> [-DESCR(D, P), show_line("\nReceived belief DESCR(",D,") from ", A), refuse()]
        +DESCR(D, P)[{'from': A}] >> [-DESCR(D, P), show_line("\nReceived belief DESCR(",D,") from ", A), accept()]

        # Non-Related-Plan assessment
        +DESCR(D)[{'from': A}] / ack_noplan(D) >> [-DESCR(D), show_line("\nReceived belief DESCR(", D, ") from ", A), refuse()]
        +DESCR(D)[{'from': A}] >> [-DESCR(D), show_line("\nReceived belief DESCR(", D, ") from ", A), accept()]

        accept() >> [show_line("\n>>>>>>>> Accepting plan <<<<<<<<<<\n"), +ACK("TRUE")[{'to': 'main'}]]
        refuse() >> [show_line("\n>>>>>>>> Refusing plan <<<<<<<<<<\n"), +ACK("FALSE")[{'to': 'main'}]]

    return type(class_name, (Agent,), {"main": main})


# custom agent rocco
globals()["Metaval"] = create_agent("Metaval")
instance = globals()["Metaval"]()


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------


# Custom agent
instance = globals()["Metaval"]()
instance.start()


class main(Agent):
    def main(self):

        # Plan assessment delegation to agent Metaval
        # init() >> [show_line("\nAchieving img description. Waiting...\n"), achieve_img_descr(), setup()]
        # setup() / DESCR(D) >> [show_line("\nImage description achieved: ", D), formulate_goal(D), achieve_plan()]
        # achieve_plan() / (DESCR(D) & GOAL(G)) >> [show_line("\nPlanning for the goal: ", G, " from the description ", D), formulate_plan(D, G), commit()]
        # commit() / (DESCR(D) & PLAN(P)) >> [+DESCR(D, P)[{'to': "Metaval"}], show_line("\n>>>>>>>> Communication started <<<<<<<<<\n")]
        #
        # +ACK("TRUE")[{'from': A}] / PLAN(P) >> [show_line(">>>>>>>> No objection for plan actuation <<<<<<<<"), actuate_plan(P), clear()]
        # +ACK("FALSE")[{'from': A}] / PLAN(P) >> [show_line(">>>>>>>> The plan cannot be actuated due to privacy issues <<<<<<<<"), clear()]
        #
        # clear() / (DESCR(D) & GOAL(G) & PLAN(P)) >> [-DESCR(D), -GOAL(G), -PLAN(P)]

        # Scenario assessment delegation to agent Metaval
        init() >> [show_line("\nAchieving img description. Waiting...\n"), achieve_img_descr(), setup()]
        setup() / DESCR(D) >> [show_line("\n>>>>>>>> Communication started <<<<<<<<<\n"), +DESCR(D)[{'to': "Metaval"}], formulate_goal(D), achieve_plan()]

        achieve_plan() / (DESCR(D) & GOAL(G)) >> [show_line("\nPlanning for the goal: ", G, " from the description ", D), formulate_plan(D, G)]

        +ACK(X)[{'from': A}] >> [+CONSENT(X), show_line(">>>>>>>> Acknowledgment acquired ", X, " from ", A, " <<<<<<<<\n"), commit()]

        commit() / (PLAN(P) & CONSENT("TRUE")) >> [-CONSENT("TRUE"), show_line("\n>>>>>>>> No objection for plan actuation <<<<<<<<<\n"), actuate_plan(P), clear()]
        commit() / (PLAN(P) & CONSENT("FALSE")) >> [-CONSENT("FALSE"), show_line("\n>>>>>>>> The plan cannot be actuated due to privacy issues <<<<<<<<<\n"), clear()]
        commit() / PLAN(P) >> [commit(), show_line(">>>>>>>> WAITING...........")]
        clear() / (DESCR(D) & GOAL(G) & PLAN(P)) >> [-DESCR(D), -GOAL(G), -PLAN(P)]

main().start()

# PHIDIAS.achieve(init(), "main")