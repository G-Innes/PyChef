import re
from rich.console import Console
import getpass
import hashlib
import os
import sys


def validate_username(username):
    """
    Validate username format & regex matching
    Args:
        username: user input from get_valid_username
    Returns:
        False: if username < 3 chars
        False: if re.match returns as None
        True: if pattern match found

    """
    if len(username) < 3:
        return False
    pattern = r"^[A-Za-z0-9]+$" # Sets regex pattern for username (only include upper/lowercase & numbers)
    return re.match(pattern, username)


def validate_password(password):
    """
    validates the password format using regular expressions.
    also checks whether the password contains a colon.
    Args:
        password: user input from get_valid_password
    Returns:
        False: if ':' found (as this is seperator in .txt file)
        False: if re.match returns as None
        True: if pattern match found
    """
    if ":" in password:
        return False
    # Ensures password includes upper & lowercase, a digit and a special char
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$" 
    return re.match(pattern, password) 


def get_valid_username():
    """
    prompts the user for a username and keeps asking until a valid username is entered.
    Args: None
    Returns:
        username: user input for username choice
    """
    console = Console()
    while True:
        username = input("Enter Username (at least 3 characters): ")
        if validate_username(username):
            return username
        else:
            console.print("Invalid username! (must be at least 3 alphanumeric characters)", style="bold red")


def get_valid_password():
    """
    Prompts the user for a password, compares password and confirmation before calling validate_pasword
    Loop continues until validate_password returns as True
    Args: None
    Returns:
        password: user input for password choice
    """
    console = Console()
    while True:
        password = getpass.getpass("Enter Strong Password: ")
        confirm_password = getpass.getpass("Confirm Password: ") # Password masking to hide entry
        if password == confirm_password: # compares password & confirmation
            if validate_password(password):
                return password
            else:
                console.print(
                    "Password must contain upper & lower case letters, 1 digit & a special symbol.",
                    style="bold red",
                )
        else:
            console.print("Passwords do not match!", style="bold red")


def signup():
    """
    calls relevant validation functions before calling save_credentials with valid username & password
    Args: None
    Returns: None
    """
    username = get_valid_username()
    password = get_valid_password()
    save_credentials(username, password)


def login():
    """
    Login function takes entered password and hashes before comparing hashed passwords
    Args: None
    Returns: None
    """
    console = Console()
    while True:
        username = input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")
        stored_credentials = read_credentials_file()
        stored_password = stored_credentials.get(username) # gets value for username key (password)
        entered_password = encrypt_password(password)  # Hash the entered password
        if stored_password and entered_password == stored_password: # Compare hashed paswords
            console.print("Login Successful", style="bold green")
            break
        else:
            console.print("Login Failed", style="bold red")
            if input("Try again? y/n: ") != "n": # Add error handling to this
                continue
            else:
                sys.exit(console.print("Program Terminated", style="bold red"))


def save_credentials(username, password):
    """
    This function calls encryption and is_username_taken functions before saving both credentials to 'credentials.txt'.
    Args:
        username: validated username from signup function
        password: validated password from signup function
    Raises:
        IOError: prints message for any accessability problems with the file
    """
    console = Console()
    encrypted_password = encrypt_password(password) # Calls encrypt function with password
    if is_username_taken(username):
        console.print(
            "Username already exists. Please choose a different username.",
            style="bold red",
        )
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
            console.print(
                "Error! Unable to write to 'credentials.txt'.", style="bold red"
            )


def is_username_taken(username):
    '''
    Checks if username already exists in file
    Args: 
        username: validated username
    Returns:
        True: if username already in file
        False: if not
    '''
    credentials = read_credentials_file()
    return username in credentials


def read_credentials_file():
    """
    This function reads the 'credentials.txt' file and returns the credentials
    in a dictionary format.
    Args: None
    Returns:
        credentials: dictionary of usernames (Keys) and passwords (Values)
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
                credentials[username] = password.rstrip("\n")
    except IOError:
        console.print("Error! Unable to read 'credentials.txt'.", style="bold red")
    return credentials


def encrypt_password(password):
    """
    This function encrypts the password using the SHA256 algorithm.
    Args:
        password: validated password
    Returns:
        sha256 hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()
