from actions import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars("D", "G",  "P", "A", "X")

# Image description reactor
class DESCR(Reactor): pass


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------

class main(Agent):
    def main(self):

        init() >> [show_line("\nAchieving img description. Waiting...\n"), achieve_img_descr()]

        +DESCR(D) >> [show_line("\nImage description achieved: ", D), formulate_goal(D)]
        +GOAL(D, G) >> [show_line("\nPlanning for the goal: ", G ," from the description ", D), formulate_plan(D, G)]
        +PLAN(D, G, P) >> [show_line("\nActions implementation the plan ", P, " to achieve the goal ", G, " from the scenario ",D), formulate_action(D, G, P)]
        +ACTUATION(D, G, P, A) / ack_plan(D, P) >> [show_line("\nNo objection."), actuate_plan(P, A)]
        +ACTUATION(D, G, P, A) >> [show_line("\nThe plan cannot be actuated.")]

main().start()

# PHIDIAS.achieve(init(), "main")
