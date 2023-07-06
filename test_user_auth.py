import pytest
import user_auth
from unittest import mock
import os
import csv
from ingredient_manager import load_ingredients, add_ingredient

from unittest.mock import patch
from api_handler import get_recipe_based_on_ingredients, get_recipe_steps


@pytest.fixture
def username():
    return 'test_username'

@pytest.fixture
def password():
    return 'Test@1234'

def test_validate_password(password):
    """
    Test the password validation function. A password that satisfies all conditions
    should be considered valid.
    """
    result = user_auth.validate_password(password)
    assert result is not None


@mock.patch('user_auth.is_username_taken', create=True)
@mock.patch('user_auth.Console.print', create=True)
def test_save_credentials(print, is_username_taken, username, password):
    """
    Test the save credentials function. If a username is not taken, it should save
    the username and password to credentials.txt and print "Registration Successful!".
    """
    is_username_taken.return_value = False
    user_auth.save_credentials(username, password)
    with open("credentials.txt", "r") as file:
        credentials = file.read()
        assert f"{username}:{user_auth.encrypt_password(password)}" in credentials
    print.assert_called_with("Registration Successful!", style="bold green")
    os.remove("credentials.txt")  # Cleanup


@pytest.fixture
def create_test_file():
    test_file_path = 'test_file.csv'
    with open(test_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['apple', 10])
        writer.writerow(['banana', 20])
    yield test_file_path
    os.remove(test_file_path)


def test_load_ingredients(create_test_file):
    test_file_path = create_test_file
    ingredients = load_ingredients(test_file_path)
    expected_ingredients = {'apple': 10.0, 'banana': 20.0}
    assert ingredients == expected_ingredients, f"Expected {expected_ingredients}, but got {ingredients}"


def test_add_ingredient(create_test_file):
    test_file_path = create_test_file
    add_ingredient(test_file_path, 'cherry', 30)
    ingredients = load_ingredients(test_file_path)
    expected_ingredients = {'apple': 10.0, 'banana': 20.0, 'cherry': 30.0}
    assert ingredients == expected_ingredients, f"Expected {expected_ingredients}, but got {ingredients}"



@patch('api_handler.send_request')
@patch('api_handler.get_recipe_steps')
def test_get_recipe_based_on_ingredients(mock_get_recipe_steps, mock_send_request):
    mock_send_request.return_value = [
        {
            'id': 123,
            'title': 'Test Recipe',
            'usedIngredients': [{'name': 'apple', 'amount': 1.0}],
            'missedIngredients': []
        }
    ]

    mock_get_recipe_steps.return_value = ['Step 1: Test Step 1', 'Step 2: Test Step 2']
    
    ingredients = 'apple,1.0'
    recipe = get_recipe_based_on_ingredients(ingredients)
    
    expected_recipe = {
        'title': 'Test Recipe',
        'ingredients': [{'name': 'apple', 'amount': 1.0}],
        'steps': ['Step 1: Test Step 1', 'Step 2: Test Step 2']
    }
    assert recipe == expected_recipe, f"Expected {expected_recipe}, but got {recipe}"


@patch('api_handler.send_request')
def test_get_recipe_steps(mock_send_request):
    mock_send_request.return_value = [
        {
            'name': 'Instructions',
            'steps': [
                {'number': 1, 'step': 'Test Step 1'},
                {'number': 2, 'step': 'Test Step 2'},
            ]
        }
    ]

    steps = get_recipe_steps(123)
    expected_steps = ['Step 1: Test Step 1', 'Step 2: Test Step 2']
    assert steps == expected_steps, f"Expected {expected_steps}, but got {steps}"
