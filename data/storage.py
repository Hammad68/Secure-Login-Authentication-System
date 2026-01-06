import json
import os

# --- FIX PYTHON PATH SO USERS DATABASE FILE CAN BE ACCESSIBLE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
userfile = os.path.join(BASE_DIR, "users.json")
# ---------------------------------------

# To load the JSON file's content
def load_users():
    if not os.path.exists(userfile):
        return {}
    with open(userfile, 'r') as f:
        return json.load(f)

# To save the JSON file after update its content
def users_save_data(data):
    with open(userfile, 'w') as f:
        json.dump(data, f, indent=4)