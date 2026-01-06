import json
import os
import time

# --- FIX PYTHON PATH SO VERIFICATION.JSON FILE CAN BE ACCESSIBLE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bruteforefile = os.path.join(BASE_DIR, "verification.json")
# ---------------------------------------

max_attempts = 3
lock_time = 30

# To load the JSON file's content
def load_bruteforcefile():
    if not os.path.exists(bruteforefile):
        return {}
    with open(bruteforefile, 'r') as f:
        return json.load(f)
    
# Initialize the user account with specific format in the JSON Database
def init_user(data, user):
    if user not in data:
        data[user] = {
            'password_fails': 0, 
            'otp_failed': 0,  
            'locked_until': 0
        }
    
# To record the otp failures for a user account
def record_otp_failed(user):
    data = load_bruteforcefile()
    init_user(data, user)

    user_data = data[user]
    current_time = time.time()

    if current_time < data[user]['locked_until']:
        return 'locked'
    
    user_data['otp_failed'] += 1

    if user_data['otp_failed'] >= max_attempts:
        user_data['locked_until'] = current_time + lock_time
        user_data['otp_failed'] = 0
        save_data(data)
        return 'locked_now'
    
    save_data(data)
    return 'failed'

# To record the password failures for a user account
def record_password_failed(user):
    data = load_bruteforcefile()
    init_user(data, user)

    user_data = data[user]
    current_time = time.time()

    if current_time < data[user]['locked_until']:
        return 'locked'
    
    user_data['password_fails'] += 1

    if user_data['password_fails'] >= max_attempts:
        user_data['locked_until'] = current_time + lock_time
        user_data['password_fails'] = 0
        save_data(data)
        return 'locked_now'
    
    save_data(data)
    return 'failed'

# To save the JSON file after update its content
def save_data(data):
    with open(bruteforefile, 'w') as f:
        json.dump(data, f, indent=4)

# To check if the user account is locked or not
def account_locked(user):
    data = load_bruteforcefile()
    if user not in data:
        return False
    return time.time() < data[user]['locked_until']

# To reset the password & otp counters in the JSON Database
def reset_account(user):
    data = load_bruteforcefile()
    init_user(data, user)
    data[user] = {'password_fails': 0, 'otp_failed': 0, 'locked_until': 0}
    save_data(data)