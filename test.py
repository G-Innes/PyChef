import pytest
import os
import csv
from ingredient_manager import load_ingredients, add_ingredient
import user_auth

@pytest.fixture
def username():
    return "test_username"


@pytest.fixture
def password():
    return "Test@1234"


def test_validate_password(password):
    """
    Password that satisfies all conditions
    should be considered valid.
    """
    result = user_auth.validate_password(password)
    assert result is not None


@pytest.fixture
def create_test_file():
    '''
    test CSV file with some sample data and returns the file path.
    '''
    test_file_path = "test_file.csv"
    with open(test_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["apple", 10])
        writer.writerow(["banana", 20])
    yield test_file_path
    os.remove(test_file_path)


def test_load_ingredients(create_test_file):
    """
    Load the ingredients from a CSV file
    and return them as a dictionary.
    """
    test_file_path = create_test_file
    ingredients = load_ingredients(test_file_path)
    expected_ingredients = {"apple": 10.0, "banana": 20.0}
    assert (
        ingredients == expected_ingredients
    ), f"Expected {expected_ingredients}, but got {ingredients}"


def test_add_ingredient(create_test_file):
    """
    Add a new ingredient to the CSV file.
    """
    test_file_path = create_test_file
    add_ingredient(test_file_path, "cherry", 30)
    ingredients = load_ingredients(test_file_path)
    expected_ingredients = {"apple": 10.0, "banana": 20.0, "cherry": 30.0}
    assert (
        ingredients == expected_ingredients
    ), f"Expected {expected_ingredients}, but got {ingredients}"
