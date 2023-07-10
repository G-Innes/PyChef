from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


def print_ingredient_stock(ingredients):
    '''
    Function for printing the users current ingredient stock in a table format
    Args:
        ingredients: users current ingredients
    Returns: None
    '''
    console = Console()
    # Creates table for user ingredients
    table = Table(
        show_header=True, header_style="bold bright_yellow", border_style="blue"
    )
    table.add_column("Ingredient", style="cyan")
    table.add_column("Quantity", style="cyan")

    for ingredient, quantity in ingredients.items():
        table.add_row(ingredient, str(quantity))

    console.print("\nCurrent ingredient stock:")
    console.print(table)


def print_recipe_steps(steps):
    '''
    Function for printing the recipe steps with styling
    Args:
        steps: recipe steps from api
        Returns: None
    '''
    console = Console()
    for step in steps:
        markdown_step = Markdown(f"{step}")
        panel = Panel(markdown_step, border_style="blue")
        console.print(panel, justify="center", style="bright_yellow")


def print_recipe(recipe):
    '''
    Formats and prints the generated recipe from inspire option with styling
    Args:
        recipe: contents of recipe generated from api call (get_recipe_by_cuisine)
    Returns: None
    '''
    console = Console()

    recipe_md = f"## {recipe['title']}\n\n"

    recipe_md += "### Ingredients:\n"
    for ingredient in recipe["ingredients"]:
        recipe_md += f"- {ingredient['name']}: {ingredient['amount']}\n"

    recipe_md += "\n### Steps:\n"
    for i, step in enumerate(recipe["steps"]):
        recipe_md += f"{i+1}. {step}\n"

    panel = Panel(Markdown(recipe_md), style="bright_yellow", border_style="blue")
    console.print(panel)
