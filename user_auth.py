import re
from rich.console import Console
import getpass
import hashlib
import os
import sys


def validate_username(username):
    '''
    Validate username format
    '''
    if len(username) < 3:
        return False
    pattern = r'^[A-Za-z0-9]+$'
    return re.match(pattern, username) is not None
    

def validate_password(password):
    '''
    validates the password format using regular expressions.
    also checks whether the password contains a colon.
    '''
    if ":" in password:
        return False
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
    return re.match(pattern, password)


def get_valid_username():
    '''
    prompts the user for a username and keeps asking until a valid username is entered.
    '''
    console = Console()
    while True:
        username = input("Enter Username (at least 3 characters): ")
        if validate_username(username):
            return username
        else:
            console.print("Invalid username! Please try again.", style="bold red")


def get_valid_password():
    '''
    the user for a password and keeps asking until a valid password is entered and confirmed.
    '''
    console = Console()
    while True:
        password = getpass.getpass("Enter Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")
        if password == confirm_password:
            if validate_password(password):
                return password
            else:
                console.print("Password must contain upper & lower case letters, 1 digit & a special symbol.", style="bold red")
        else:
            console.print("Passwords do not match!", style="bold red")


def signup():
    '''calls relevant validation functions before calling save credentials'''
    username = get_valid_username()
    password = get_valid_password()
    save_credentials(username, password)


def login():
    '''login function takes entered password and hashes before comparing hashed passwords'''
    console = Console()
    while True:
        username = input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")
        stored_credentials = read_credentials_file()
        stored_password = stored_credentials.get(username)
        entered_password = encrypt_password(password)  # Hash the entered password
        if stored_password and entered_password == stored_password:
            console.print("Login Successful", style="bold green")
            break
        else:
            console.print("Login Failed", style="bold red")
            if input("Try again? y/n: ") != "n":
                continue
            else:
                sys.exit(console.print("Program Terminated", style="bold red"))


def save_credentials(username, password):
    """
    This function saves the credentials to the 'credentials.txt' file.
    """
    console = Console()
    encrypted_password = encrypt_password(password)
    if is_username_taken(username):
        console.print("Username already exists. Please choose a different username.", style="bold red")
    else:
        try:
            file_path = os.path.join(os.path.dirname(__file__), "credentials.txt")
            if not os.path.exists(file_path):
                with open(file_path, "w"):
                    pass

            credentials = read_credentials_file()
            credentials[username] = encrypted_password

            with open(file_path, "w") as file:
                for user, pw in credentials.items():
                    file.write(f"{user}:{pw}\n")

            console.print("Registration Successful!", style="bold green")
        except IOError:
            console.print("Error! Unable to write to 'credentials.txt'.", style="bold red")


def is_username_taken(username):
    credentials = read_credentials_file()
    return username in credentials


def read_credentials_file():
    """
    This function reads the 'credentials.txt' file and returns the credentials
    in a dictionary format.
    """
    console = Console()
    credentials = {}
    try:
        file_path = os.path.join(os.path.dirname(__file__), "credentials.txt")
        if not os.path.exists(file_path):
            return credentials

        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split(":", 1)
                credentials[username] = password.rstrip('\n')
    except IOError:
        console.print("Error! Unable to read 'credentials.txt'.", style="bold red")
    return credentials



def encrypt_password(password):
    '''
    This function encrypts the password using the SHA256 algorithm.
    '''
    return hashlib.sha256(password.encode()).hexdigest()