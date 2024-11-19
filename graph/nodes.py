from typing import Literal
import json

from llm.llm import get_recipe_suggestions, get_recipe_details
from graph.state import AgentState

def node_input_ingredients(state):
    print("Welcome to the Cooking Chatbot! Please provide at least four ingredients (comma-separated).")
    ingredients = input("What ingredients do you have?").lower()
    state["ingredients"] = ingredients.split(",")
    return {"ingredients": ingredients.split(","), "suggestions": [], "current_node": "", "previous_suggestions": []  }

def node_validate_ingredients(state: AgentState)->Literal["Suggest Recipe", "Input Ingredients"]:
    print("Verifying your input!...")

def node_suggest_recipes(state: AgentState):
    print("Current State:",state)
    suggestions = get_recipe_suggestions(state["ingredients"], state["previous_suggestions"])
    state["suggestions"] = suggestions
    current_recipe_suggestion_name = json.loads(suggestions)

    state["previous_suggestions"] = state["previous_suggestions"].append(current_recipe_suggestion_name["name"])
    print("Here is a recipe suggestion:\n", suggestions)
    return {'suggestions': suggestions}

def node_confirm_choice(state):
    print("Do you like this recipe?")

def node_get_recipe_details(state):
    recipe_details = get_recipe_details(state['ingredients'], state['suggestions'])
    print("Here is a recipe suggestion:\n", recipe_details)
    return { "current_node": "Get Recipe Details"}

def node_retry(state):
    return {"message": "Would you like to try again with different ingredients?"}

def node_end(state):
    print("Good Bye!")
    return {"current_node": "End"}