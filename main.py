import sys
from rich.console import Console
import ingredient_manager
import user_auth
from inspire import inspire_me
from api_handler import run
from save_handler import save_recipe, view_saved_recipes
from print_handler import print_ingredient_stock


def main():
    """
    sets the file path for ingredients, calls authenticate first and then starts loop for main menu
    
    """
    file_path = "ingredients.csv"
    authenticate()
    ingredients = {}
    while True:
        main_menu(file_path, ingredients)


def get_valid_input(prompt, valid_choices, error_message):
    """
    Helper function that prompts the user for input and keeps asking until a valid choice is made.
    Args:
        prompt: user input message
        valid_choices: list of options for user
        error_message: invalid choice message
    Returns:
            user choice from list of options
    Raises:
    """
    console = Console()
    while True:
        choice = input(prompt).lower()
        print()
        if choice in valid_choices:
            return choice
        else:
            console.print(error_message, style="bold red")


def authenticate():
    """
    This function displays the login portal and allows the user to sign up,
    login, or exit the program. Its calls the validate input function then
    the signup and login functions from the user_auth module.
    Args: None
    Returns: None
    """
    console = Console()
    while True:
        console.print(
            "---  Login Portal  ---",
            style="bold blue on bright_yellow",
            justify="center",
        )
        print()
        console.print("1. Login", style="bright_yellow", justify="center")
        console.print("2. Signup", style="bright_yellow", justify="center")
        console.print("3. Quick Access", style="grey23", justify="center")
        print()
        console.print("'q' Exit", style="bright_yellow", justify="center")
        print()
        # Set params for helper function & call
        prompt = "Enter your choice: "
        valid_choices = ["1", "2", "3", "q"]
        error_message = "Invalid choice! Please enter a number between 1 and 5."
        choice = get_valid_input(prompt, valid_choices, error_message)
        # Break to main menu on succsesful login
        if choice == "1":
            user_auth.login()
            break
        elif choice == "2":
            user_auth.signup()
        elif choice == "3":
            break
        elif choice == "q":
            sys.exit(console.print("Program Terminated", style="bold red"))


def main_menu(file_path, ingredients):
    """
    Displays the main menu and handles the user's choice with the helper function.
    It allows the user to update ingredients, generate a recipe, view saved
    recipes, add preferences & get inspired by a random recipe.
    Args:
        file_path: the file path for ingredients.txt
        ingredients: content from ingredients.txtr
    Returns: None
    """
    console = Console()
    ingredients = ingredient_manager.load_ingredients(file_path) 
    while True:
        console.print(
            "---  :snake: PyChef :snake:  ---",
            style="bold blue on bright_yellow",
            justify="center",
        )
        print()
        console.print("1. Update Ingredients", style="bright_yellow", justify="center")
        console.print(
            "2. Generate Recipe From Ingredients",
            style="bright_yellow",
            justify="center",
        )
        console.print("3. Inspire Me", style="bright_yellow", justify="center")
        console.print("4. View Saved Recipes", style="bright_yellow", justify="center")
        console.print("5. Show Current Ingredient Stock", style="bright_yellow", justify="center")
        print()
        console.print("'q' Exit", style="bright_yellow", justify="center")
        print()

        prompt = "Enter your choice (1-5 or 'q'): "
        valid_choices = ["1", "2", "3", "4", "5", "q"]
        error_message = (
            "Invalid choice. Please enter a number between 1 and 5, or 'q' to exit."
        )
        choice = get_valid_input(prompt, valid_choices, error_message)

        if choice == "1":
            update_prompt = "Enter 1 to add or 2 to remove ingredient: "
            update_valid_choices = ["1", "2"]
            update_error_message = (
                "Invalid choice. Please enter '1' to add or '2' to remove."
            )
            update_choice = get_valid_input(
                update_prompt, update_valid_choices, update_error_message
            )
            # get ingredient, quantity & pass to function with the file path for ingredients.txt.
            if update_choice == "1":
                ingredient = input("Enter the ingredient to add: ")
                try:
                    quantity = float(input("Enter the quantity to add: "))
                    ingredient_manager.add_ingredient(file_path, ingredient, quantity)
                except ValueError:
                    print("Invalid quantity. Please enter a number.")

            if update_choice == "2":
                while True:
                    name = input("Enter the ingredient to remove: ")
                    quantity = float(input("Enter the quantity to remove: "))
                    # Check if ingredient exists & greater than 0 before function call with args.
                    if name.strip() and float(quantity) and int(quantity) > 0:
                        ingredient_manager.remove_ingredient(file_path, name, quantity)
                        break
                    else:
                        console.print(
                            "Invalid name or quantity. Please try again.",
                            style="bold red",
                        )
        # load ingredients and pass to api_handler function.
        elif choice == "2":
            ingredients = ingredient_manager.load_ingredients(file_path)
            recipe = run(ingredients)
            if recipe is not None:  # If there is recipe prompts to save & calls save function.
                prompt = "Do you want to save this recipe? (y/n): "
                valid_choices = ["y", "n"]
                error_message = (
                    "Invalid choice! Please enter 'y' f or yes or 'n' for no."
                )
                save_choice = get_valid_input(prompt, valid_choices, error_message)
                if save_choice == "y":
                    save_recipe(recipe)

        elif choice == "3":
            inspire_me()

        elif choice == "4":
            view_saved_recipes()

        elif choice == "5":
            print_ingredient_stock(ingredients)

        elif choice == "q":
            sys.exit(console.print("Program Terminated", style="bold red"))


if __name__ == "__main__":
    main()
