from components.strength import strength_checker
from components.hashing import hash_bcrypt
from components.authentication import generate_totp_secret
from data.storage import load_users, users_save_data
from auditing.audit import log_event
import re

# Function to register a new user
def register():

    # Loading the users data from the database file
    users = load_users()

    print('REGISTRATION OF NEW USER')

    # Taking user input for username
    username = input('Enter Username: ').strip().lower()

    # If username is empty
    if not username:
        print('Username Must Be Non-Empty')
        return
    
    # To make sure that username consists of valid format
    if not valid_username(username):
        print('Username must be 3–20 chars, lowercase letters, numbers, underscore')
        return

    # Checking if username already exists in the database, if it does then exit the function
    if username in users:
        log_event("REGISTRATION_FAILED", username, "Username already exists")
        print('Username Already Exists')
        return
    
    # If usenname does not exist in the database 
    while True:

        # Taking user password input for checking password strength
        password = input('Enter password: ').strip()
        score, entropy = strength_checker(password)

        # To see if password is same as username
        if password.lower() == username:
            print('Password Must Be Different From Username')
            log_event("REGISTRATION_ATTEMPT", username, "Password equals username")
            continue

        # Checking minimum strength specified by the score then hash it and store the hash in database
        if score >= 5:
            secret = generate_totp_secret(username)
            hash = hash_bcrypt(password).decode()

            users[username] = {
                'hash': hash,
                'secret': secret
            }
            users_save_data(users)
            log_event("USER_REGISTERED", username, "New user registered")
            print('Registration Successful')
            return

        # If password is week then let the user know
        print('Password Not Strong, Try Again')
        log_event("REGISTRATION_ATTEMPT", username, "Password strength below threshold")


# To decide if the username format is right or not
def valid_username(username: str) -> bool:
    USERNAME_REGEX = re.compile(r'^[a-z][a-z0-9_]{2,19}$')
    return bool(USERNAME_REGEX.match(username))

        