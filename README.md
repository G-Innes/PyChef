# PyChef

PyChef is a comprehensive recipe assistant designed to inspire your cooking adventures. With features like user authentication, ingredient management, recipe suggestions, adding favourites, PyChef enables you to discover new recipes with ease.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Getting Started](#getting-started)
4. [Running the Application](#running-the-application)
5. [Testing](#testing)
6. [Contribution](#contribution)
7. [Future Scope](#future-scope)

<a name="features"></a>
## Features

### Authentication
Users can sign up and log into the application, with password encryption providing secure access.

### Ingredient Management
Keep track of your kitchen supplies by adding or removing ingredients from your inventory.

### Recipe Suggestions
PyChef uses the Spoonacular API to suggest recipes based on your stocked ingredients.

### Inspire Me
If you're open to trying something new, you can generate a recipe based on a cuisine type.

### Favourites Management
Save your favourite recipes for easy access in the future, and view them anytime.

<a name="prerequisites"></a>
## Prerequisites

PyChef requires Python 3.8 or later, and the following Python libraries:

- `rich`
- `requests`
- `os`
- `hashlib`
- `getpass`
- `re`
- `sys`
- `random`
- `dotenv`
- `csv`
- `pytest` for running the tests


Additionally, you'll need to create a free account on [Spoonacular](https://spoonacular.com/food-api) to obtain an API key. Once you have the key, create a `.env` file and store the key as follows:

API_KEY=your_api_key


<a name="getting-started"></a>
## Getting Started

Clone the repository to your local machine:

git clone https://github.com/TuringCollegeSubmissions/ginnes-FPCS.4.git


<a name="running-the-application"></a>
## Running the Application

To start PyChef, run the `main.py` script:

python3 main.py

Ensure that you've added some ingredients to your inventory before trying to generate a recipe.

<a name="testing"></a>
## Testing

The `pytest` module is used for testing in PyChef. Run the tests with the following command:

pytest test.py

<a name="contribution"></a>
## Contribution

Contributions are welcome! For major changes, please open an issue first to discuss the proposed change.

<a name="future-scope"></a>
## Future Scope

There are several potential enhancements for PyChef, including sharing favourite recipes, adding dietary requirements, incorporating meal plans, and more. Stay tuned for updates!