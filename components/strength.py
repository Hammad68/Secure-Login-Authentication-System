import math
import string
import os

# --- FIX PYTHON PATH SO Password FILE CAN BE ACCESSIBLE ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COMMON_PATH = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "attackSimulation", "commonPasswords.txt")
)
# ---------------------------------------
# Load list of Common passwords
with open(COMMON_PATH, "r") as f:
    COMMON_PASSWORDS = {line.strip().lower() for line in f}
# ---------------------------------------


# For Checking the password strength
def strength_checker(password: str):
    """Checking the password's strength based on its length and character variety"""

    # If len(password) < 8 then return score = 0, entropy = 0 
    if len(password) < 12:
        print('Week Password - Use A Longer Password - Length Is Less Than 12 Characters')
        return 0, 0
    # Checking again week and common passwords
    if password.lower() in COMMON_PASSWORDS:
        print('Very Common Password - Use Another One')
        return 0, 0    

    # Rewarding for password len equal or more than 12
    score = 0
    if len(password) >= 12:
        score += 1
    # Checking the variety of characters
    char_pool = 0
    if any(c.islower() for c in password):
        char_pool += 26
    if any(c.isupper() for c in password):
        char_pool += 26
    if any(c.isdigit() for c in password):
        char_pool += 10
    if any(c in string.punctuation for c in password):
        char_pool += len(string.punctuation)
    if char_pool < 94:
        print("Password must include upper, lower, number, and symbol")
        return 0, 0

    # Finalizing score and entropy
    score += 4
    entropy = len(password) * math.log2(char_pool)
    return score, round(entropy, 2)