from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print


def print_ingredients(ingredients):
    """
    Prints the names and measurements of the given ingredients.
    """
    for ingredient in ingredients:
        print(f"- Name: {ingredient['name']}")
        print(f"  Measurement: {ingredient['amount']}")
        print()

def print_ingredient_stock(ingredients):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Ingredient", style="cyan")
    table.add_column("Quantity", style="cyan")

    for ingredient, quantity in ingredients.items():
        table.add_row(ingredient, str(quantity))

    console.print("\nCurrent ingredient stock:")
    console.print(table)

def print_recipe_steps(steps):
    console = Console()
    for step in steps:
        markdown_step = Markdown(f"{step}")
        panel = Panel(markdown_step)
        console.print(panel)

def print_recipe(recipe):
    console = Console()
    
    recipe_md = f"## {recipe['title']}\n\n"

    recipe_md += "### Ingredients:\n"
    for ingredient in recipe['ingredients']:
        recipe_md += f"- {ingredient['name']}: {ingredient['amount']}\n"

    recipe_md += "\n### Steps:\n"
    for i, step in enumerate(recipe['steps']):
        recipe_md += f"{i+1}. {step}\n"

    console.print(Markdown(recipe_md))












