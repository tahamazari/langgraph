import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_recipe_suggestions_prompt(user_ingredients, previous_suggestions):
    previous_suggestions_str = ""
    if previous_suggestions:
        previous_suggestions_str = (
            "Avoid suggesting dishes similar to the following previous suggestions:\n" +
            ", ".join(previous_suggestions) + "\n"
        )
    return (
        "You are a helpful cooking assistant. Suggest a single dish based on the ingredients provided.\n"
        "Include only dishes that use at least four of the listed ingredients.\n"
        "Common condiments like oil, salt, and water are always available.\n"
        "Provide just the dish name and with one line as description.\n"
        "Also, return in form of json like -> { name, description } two keys\n"
        f"{previous_suggestions_str}"
        f"My ingredients are: {', '.join(user_ingredients)}"
    )

def get_recipe_prompt(user_ingredients, recipe_suggestion):
    return (
        "You are a helpful cooking assistant. Tell me how to make the following dish.\n"
        "Common condiments like oil, salt, and water are always available.\n"
        f"I have these ingredients: {', '.join(recipe_suggestion)}"
        f"The name and description is: {', '.join(user_ingredients)}"
    )

# Function to get recipe suggestions from ChatGPT
def get_recipe_suggestions(user_ingredients, previous_suggestions):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": get_recipe_suggestions_prompt(user_ingredients, previous_suggestions)}],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:  # Catch OpenAI-specific errors
        return f"Error communicating with OpenAI: {e}"
    except Exception as e:  # Catch other potential errors
        return f"An unexpected error occurred: {e}"
    
def get_recipe_details(recipe_suggestion, user_ingredients):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": get_recipe_prompt(recipe_suggestion, user_ingredients)}],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:  # Catch OpenAI-specific errors
        return f"Error communicating with OpenAI: {e}"
    except Exception as e:  # Catch other potential errors
        return f"An unexpected error occurred: {e}"