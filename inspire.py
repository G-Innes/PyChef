from api_handler import get_random_recipe_by_cuisine
from print_handler import print_recipe
from save_handler import save_recipe


def inspire_me():
    '''
    Prompt user & pass cuisine to API function
    Args: None
    Returns: None
    '''
    cuisine = input("Enter the cuisine type: ")
    recipe = get_random_recipe_by_cuisine(cuisine)
    # If recipe is found, give option to save
    if recipe:
        print_recipe(recipe)
        save_choice = input("Do you want to save this recipe? (y/n): ")
        if save_choice.lower() == "y":
            save_recipe(recipe)
