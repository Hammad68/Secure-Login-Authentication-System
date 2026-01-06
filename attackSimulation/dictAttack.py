import os
import bcrypt
import sys
from data.storage import load_users

# --- FIX PYTHON PATH SO IMPORTS WORK ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
# ---------------------------------------

def dict_attack(username, passwords, results):
    """Performing the dictionary attack to guess the password"""

    # Loading the users from our JSON database
    users = load_users()

    # If username exists in the database
    if username not in users:
        print('Unknown User')
        return

    # Storing the user's password hash for perfroming the attack
    stored_hash = users[username]['hash'].encode()
    print(f"\n Starting Dict Attack on user '{username}'\n")

    # Hashing each password and comparing it with stored hash
    for i in passwords:
        print(f"Trying {i}")
        password = i.encode()
        if bcrypt.checkpw(password, stored_hash):
            print(f"\n Password Found For {username}: {i}")
            results[username] = i
            return 
        
    return

def execute():
    """Executing dictionary attack on all users in our JSON database"""

    # Load password list
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "breachedPasswords.txt")

    # Using all passwords from the passwords list
    with open(file_path, 'r') as f:
        password = [i.strip() for i in f]

    # Performing dict attack on each of the users
    cracked_password = {}
    users = load_users()
    for i in users:
        dict_attack(i, password, cracked_password)

    # Summary
    print("\n=======================")
    print("DICTIONARY ATTACK SUMMARY")
    print("=======================\n")
    # Results to display
    if cracked_password:
        for user, password in cracked_password.items():
            print(f"{user}: {password}\n")
    else:
        print("No Passwords Were Cracked\n")
        return
    
    return