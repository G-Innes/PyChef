import requests
import random
import os
from dotenv import load_dotenv
from rich.table import Table
from rich.console import Console
from ingredient_manager import load_ingredients
from print_handler import print_recipe_steps, print_ingredient_stock

def get_params():
    """
    Returns the required parameters for the API requests.
    """
    load_dotenv()
    return {
        "apiKey": os.getenv("API_KEY"),
    }              

def send_request(url, params):
    """
    Sends a GET request to the specified URL with the given parameters. 
    Returns the JSON response if successful.
    """
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return None

def get_recipe_based_on_ingredients(ingredients):
    """
    Fetches recipes based on the given ingredients.
    Prints the recipe with the most matching ingredients and returns its ID.
    """
    # Set up the API endpoint URL
    url = "https://api.spoonacular.com/recipes/findByIngredients"

    params = get_params()
    params["number"] = 20
    params["ingredients"] = ingredients

    data = send_request(url, params)
  
    if data and isinstance(data, list) and len(data) > 0:
        sorted_recipes = sorted(data, key=lambda r: len(r['usedIngredients']), reverse=True)
        recipe = random.choice(sorted_recipes)

        console = Console()

        print()
        console.print(f"Recipe ID: {recipe['id']}", style="green")
        console.print(f"Title: {recipe['title']}", style="bold bright_yellow underline")
        print()

        used_table = Table(show_header=True, header_style="bold magenta")
        used_table.add_column("Your Ingredients", style="cyan", width=20)
        used_table.add_column("Quantity", style="cyan", width=10)
        for ingredient in recipe['usedIngredients']:
            used_table.add_row(ingredient['name'], str(ingredient['amount']))

        console.print(used_table)

        missing_table = Table(show_header=True, header_style="bold magenta")
        missing_table.add_column("Missing Ingredients", style="red", width=20)
        missing_table.add_column("Quantity", style="red", width=10)
        for ingredient in recipe['missedIngredients']:
            missing_table.add_row(ingredient['name'], str(ingredient['amount']))

        console.print(missing_table)

        recipe_steps = get_recipe_steps(recipe['id'])
        if recipe_steps:
            recipe['steps'] = recipe_steps

        cleaned_recipe = {
            'title': recipe['title'],
            'ingredients': [{'name': i['name'], 'amount': i['amount']} for i in recipe['usedIngredients']],
            'steps': recipe_steps
        }

        return cleaned_recipe

    print("No recipes found for the given ingredients.")
    return None

def get_recipe_steps(recipe_id):
    """
    Fetches and returns the cooking steps for the recipe with the given ID.
    """
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"

    data = send_request(url, get_params())

    if data and len(data) > 0:
        steps = [f"Step {i['number']}: {i['step']}" for i in data[0]['steps']]
        return steps

    print("No steps found for the recipe.")
    return None

def get_random_recipe_by_cuisine(cuisine_type):
    """
    Fetches a random recipe based on the given cuisine type.
    """
    url = "https://api.spoonacular.com/recipes/random"

    params = get_params()
    params["number"] = 1  
    params["tags"] = cuisine_type

    data = send_request(url, params)

    if data and 'recipes' in data and len(data['recipes']) > 0:
        recipe = data['recipes'][0]

        cleaned_recipe = {
            'title': recipe['title'],
            'ingredients': [{'name': i['name'], 'amount': i['measures']['metric']['amount']} for i in recipe['extendedIngredients']],
            'steps': [s['step'] for s in recipe['analyzedInstructions'][0]['steps']]
        }
        return cleaned_recipe

    print(f"No recipes found for the {cuisine_type} cuisine.")
    return None


def run(ingredients):
    file_path = 'ingredients.csv'
    ingredients = load_ingredients(file_path)

    if not ingredients:
        print("No ingredients found in the file.")
        return

    ingredient_names = ",".join([f"{k},{v}" for k, v in ingredients.items()])
    print_ingredient_stock(ingredients)
    recipe = get_recipe_based_on_ingredients(ingredient_names)

    if recipe:
        print_recipe_steps(recipe['steps'])
    else:
        print("Failed to get recipe based on ingredients")
    return recipe


if __name__ == "__main__":
    run()