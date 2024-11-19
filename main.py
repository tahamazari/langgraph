from langgraph.graph import StateGraph, START, END
from typing import Literal
from dotenv import load_dotenv

from graph.state import AgentState
from graph.nodes import node_input_ingredients, node_validate_ingredients, node_end, node_suggest_recipes, node_confirm_choice, node_get_recipe_details
from graph.edges import cond_edge_validate_ingredients, cond_edge_confirm_recipe_conditional 

# Create workflow
def create_cooking_workflow():
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("Input Ingredients", node_input_ingredients)
    workflow.add_node("Validate Ingredients", node_validate_ingredients)
    workflow.add_node("Suggest Recipe", node_suggest_recipes)  # Function node
    workflow.add_node("Confirm Choice", node_confirm_choice)  # Function node
    workflow.add_node("Get Recipe Details", node_get_recipe_details)
    workflow.add_node("End", node_end)

    # Edges
    workflow.add_edge(START, "Input Ingredients")
    workflow.add_edge("Input Ingredients", "Validate Ingredients")
    workflow.add_conditional_edges(
        "Validate Ingredients",
        cond_edge_validate_ingredients,
        {
            "suggest_recipe": "Suggest Recipe",
            "input_ingredients": "Input Ingredients"
        }
    )
    workflow.add_edge("Suggest Recipe", "Confirm Choice")
    workflow.add_conditional_edges(
        "Confirm Choice",
        cond_edge_confirm_recipe_conditional, 
        {
            "yes": "Get Recipe Details",
            "retry": "Suggest Recipe"
        }
    )
    workflow.add_edge("Get Recipe Details", "End")
    workflow.add_edge("End", END)

    return workflow.compile()

# Run the chatbot
def main():
    cooking_workflow = create_cooking_workflow()
    cooking_workflow.invoke({"ingredients": [], "suggestions": "", "current_node": "Welcome", "previous_suggestions": []})

if __name__ == "__main__":
    main()