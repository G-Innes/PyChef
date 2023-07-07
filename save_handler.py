import os


def save_recipe(recipe):
    """
    Save a recipe to the favorites file. appends title, ingredients & steps to favourites file
    """
    file_path = os.path.join(os.path.dirname(__file__), "favorites.txt")
    with open(file_path, "a") as f:
        f.write(f"Title: {recipe['title']}\n")
        f.write("Ingredients:\n")
        for ingredient in recipe["ingredients"]:
            f.write(f"- {ingredient['name']}: {ingredient['amount']}\n")
        f.write("Steps:\n")
        for step in recipe["steps"]:
            f.write(f"- {step}\n")
        f.write("\n")
    print("Recipe saved!")


def view_saved_recipes():
    """
    View saved recipes.
    """
    file_path = os.path.join(os.path.dirname(__file__), "favorites.txt")
    with open(file_path, "r") as f:
        print(f.read())
