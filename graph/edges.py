from typing import Literal
from graph.state import AgentState

def cond_edge_validate_ingredients(state: AgentState)->Literal["Suggest Recipe", "Input Ingredients"]:
    if len(state["ingredients"]) < 4:
        return "input_ingredients"
    return "suggest_recipe"

def cond_edge_confirm_recipe_conditional(state):
    decision = input("And you like to cook this? (yes/no): ").lower()
    if(decision == "yes"):
        return "yes"
    if(decision == "no"):
        return "retry"
    return "yes"