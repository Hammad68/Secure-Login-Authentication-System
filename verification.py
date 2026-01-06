from components.hashing import verify_bcrypt
from components.authentication import verifytotp
from data.storage import load_users
from auditing.audit import log_event
from bruteforce.rateLimiting import record_password_failed, record_otp_failed, account_locked, reset_account

# Main function responsible for authenticating the user
def verify():

    # Loading the users data from the database file
    users = load_users()

    print('VERIFYING USER')

    # Taking user input username for verification purposes
    check_username = input('Enter Your Username: ').strip().lower()

    # Checking if username is empty or if it does not exists in the database
    if not check_username:
        print('Username Must Be Non-Empty')
        return False
    if check_username not in users:
        print('Invalid Credentials.')
        log_event('INVALID_CREDENTIALS', check_username, 'Unknown Username')
        return False
    
    # If the user account has been temporarily blocked due to maximum OTP or Password attempts
    if account_locked(check_username):
        print("Account temporarily locked. Try again later.")
        log_event("ACCOUNT_LOCKED", check_username, "Login attempt while locked")
        return False
    
    # Storing user's password hash and totp secret for authentication to follow 
    stored_hash = users[check_username]['hash']
    stored_secret = users[check_username]['secret']

    # Verifying user password
    if not password_check(stored_hash, check_username):
        return False
    
    # Verifying user otp to complete authentication step
    return otp_check(stored_secret, check_username)



# Function to check if password is verified or not
def password_check(hash, username):
    while True:
        check_password = input('Enter Your Password: ').strip()
        if verify_bcrypt(check_password, hash.encode()):
            print('PASSWORD VERIFIED')
            log_event("PASSWORD_VERIFIED", username, "Correct password")
            return True
        status = record_password_failed(username)
        print("Invalid Credentials")
        log_event("INVALID_CREDENTIALS", username, "Wrong password")
        if status == "locked_now":
            print("Invalid Password — Account locked for 30 secs")
            log_event("ACCOUNT_LOCKED", username, "Too many failed password attempts")
            return False

# Function to check if otp is verified or not
def otp_check(secret, username):
    for i in range(3):
        user_otp = input('Enter OTP: ').strip()
        if verifytotp(secret, user_otp):
            print('AUTHENTICATION SUCCESSFUL')
            log_event("LOGIN_SUCCESSFUL", username, "Correct password + OTP")
            reset_account(username)
            return True
        else: 
            status = record_otp_failed (username)
            print(f'Invalid OTP, Try Again - ({i + 1}/3)')
            log_event("OTP_FAILURE", username, f"Wrong OTP attempt {i+1}")
            if status == "locked_now":
                print("Verification Failed - Account locked for 30 secs")
                log_event('MAX_LOGIN_ATTEMPTS', username, 'Exceeded OTP Attempts')
                return False
    return False