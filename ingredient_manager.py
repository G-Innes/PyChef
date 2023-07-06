import csv


def load_ingredients(file_path):
    """
    Load ingredients from a CSV file.
    Each row in the CSV file should represent an ingredient with the
    format: ingredient name, quantity.
    """
    ingredients = {}
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                ingredients[row[0]] = float(row[1])
    except FileNotFoundError:
        print("The file does not exist.")
        return ingredients
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return ingredients
    return ingredients


def add_ingredient(file_path, name, quantity):
    """
    Add a quantity of an ingredient to the list.
    If the ingredient is already present, the quantity is updated.
    The updated list of ingredients is saved to the file.
    """
    ingredients = load_ingredients(file_path)
    if name in ingredients:
        ingredients[name] += quantity
    else:
        ingredients[name] = quantity

    save_ingredients(file_path, ingredients)


def remove_ingredient(file_path, ingredient_name, quantity):
    """
    Remove a quantity of an ingredient from the list.
    If the remaining quantity of the ingredient is 0 or less,
    the ingredient is removed from the list.
    The updated list of ingredients is saved to the file.
    """
    ingredients = load_ingredients(file_path)
    if ingredient_name in ingredients:
        ingredients[ingredient_name] -= quantity
        if ingredients[ingredient_name] <= 0:
            del ingredients[ingredient_name]
    else:
        raise ValueError(f"Ingredient '{ingredient_name}' not found in the list.")

    save_ingredients(file_path, ingredients)
    
def save_ingredients(file_path, ingredients):
    """
    Save a list of ingredients to a CSV file.
    Each row in the CSV file represents an ingredient with the format:
    ingredient name, quantity.
    """
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for ingredient, quantity in ingredients.items():
                writer.writerow([ingredient, quantity])
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def get_ingredient_list(file_path):
    """
    Return a formatted string representing the list of ingredients.
    """
    ingredients = load_ingredients(file_path)
    ingredient_list = "\n".join(f"- {name} : {quantity}" for name, quantity in ingredients.items())
    return ingredient_list




