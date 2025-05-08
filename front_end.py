from actions import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars("D", "G",  "P", "A")

# Image description reactor
class DESCR(Reactor): pass


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------

class main(Agent):
    def main(self):

        # World initialization
        init() >> [show_line("\nInitialiting agent...\n"), +DESCR("Image description.") ]

        +DESCR(D) >> [show_line("\nImage description achieved: ", D), formulate_goal(D)]
        +GOAL(D, G) >> [show_line("\nPlanning for the goal ",G ," from the description ", D), formulate_plan(D, G)]
        +PLAN(D, G, P) >> [show_line("\nActions implementation the plan ", P, " to achieve the goal ",G," from the scenario ",D), formulate_action(D, G, P)]
        +ACTION(D, G, P, A) / ack_plan(D, P) >> [show_line("\nActions ", A, " implementing the plan ",P, " ready to be executed.")]

main().start()

# PHIDIAS.achieve(init(), "main")
