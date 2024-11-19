from typing import TypedDict

# State Definition
class AgentState(TypedDict):
    ingredients: list[str]  # List of user ingredients
    suggestions: str  # Recipe suggestions
    current_node: str  # Current node in the conversation
    previous_suggestions: list[str]