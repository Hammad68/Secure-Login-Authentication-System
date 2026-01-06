from data.storage import load_users, users_save_data
from components.hashing import hash_bcrypt, verify_bcrypt
from bruteforce.rateLimiting import load_bruteforcefile, save_data, account_locked, reset_account  
from verification import otp_check, password_check
from components.strength import strength_checker
from auditing.audit import log_event
import os


# Function responsible for reseting the password
def passord_reset():
    # Loading the users data from the database file
    users = load_users()

    # Taking user input for username
    username = input('Whats the username? ').strip().lower()

    # Checking if username is empty or if it does not exists in the database
    if not username:
        print('Username Must Be Non-Empty')
        return False
    if username not in users:
        print('Invalid Credential ...')
        log_event('INVALID_CREDENTIALS', username, 'Unknown Username')
        return False

    # If the user account has been temporarily blocked due to maximum OTP or Password attempts
    if account_locked(username):
        log_event("ACCOUNT_LOCKED", username, "Login attempt while locked for password reset")
        print('Account locked temporarily')
        return False
    
    # Checking if user's secret has been configured or not for OTP verification
    secert = users[username]['secret']
    if not secert:
        print('OTP not configured')
        return False
    
    # Verifying user otp to complete authentication step
    if not otp_check(secert, username):
        log_event("PASSWORD_RESET_FAILED", username, "OTP verification failed")
        return False
    
    # For setting up new password
    for _ in range(3):
        # Taking user's input for password
        new_password = input('Setup new password: ').strip()

        # Prevent password reuse
        if verify_bcrypt(new_password, users[username]['hash'].encode()):
            print("New password must be different from old password")
            log_event("PASSWORD_RESET_ATTEMPT", username, "Password reused")
            continue

        # Password must be different from username
        if new_password.lower() == username:
            print('Password must be different from username')
            log_event("PASSWORD_RESET_ATTEMPT", username, "Password equals username")
            continue

        # Checking password strength if it is above the threshold or not
        score, entropy = strength_checker(new_password)
        if score >= 5:
            users[username]['hash'] = hash_bcrypt(new_password).decode()
            users_save_data(users)

            reset_account(username)
            log_event("PASSWORD_CHANGED", username, "Account password changed")
            print('Password Has Been Reset')
            return True

        # If the password is not strong enough then let the user know
        log_event("PASSWORD_RESET_ATTEMPT", username, "Password strength below threshold")
        print('Password not strong enough')

    # If the password reset process fails completely
    log_event("PASSWORD_RESET_FAILED", username, "Password reset failed completely")
    print('Password Reset Failed')
    return False


# Function to delete an existing user
def delete_user(): 
    # Loading the data from the users database, and verification files
    users = load_users()
    verifications = load_bruteforcefile()

    # Taking the user input for username
    username = input('Whats the username? ').strip().lower()

    # Checking if username is empty or if it does not exists in the database
    if not username:
        print('Username Must Be Non-Empty')
        return False
    if username not in users:
        log_event('INVALID_CREDENTIALS', username, 'Unknown Username')
        print('Invalid Credential ...')
        return False
    
    # If the user account has been temporarily blocked due to maximum OTP or Password attempts
    if account_locked(username):
        log_event("ACCOUNT_LOCKED", username, "Login attempt while locked for password deletion")
        print("Account temporarily locked. Try again later.")
        return False

    # Storing user's password hash and totp secret for authentication to follow 
    secert = users[username]['secret']
    stored_hash = users[username]['hash']

    # Checking if user's secret has been configured or not for OTP verification
    if not secert:
        print('OTP not configured')
        return False
    
    # Verifying user password
    if not password_check(stored_hash, username):
        log_event("DELETION_FAILED", username, "Password verification failed")
        print('Account Deletion Failed')
        return False
    
    # Verifying user otp to complete authentication step
    if not otp_check(secert, username):
        log_event("DELETION_FAILED", username, "OTP verification failed")
        print('Account Deletion Failed')
        return False
    
    # Resetting the users account after password & OTP authentication 
    reset_account(users)
    
    # Deleting the user's account from users JSON file
    # And verification of that account state from verifications JSON file
    users.pop(username) 
    verifications.pop(username, None)
    # Deleting the corresponding QRcode as well
    qr_path = os.path.join('qrcodes', f'{username}_totp_setup.png')
    if os.path.exists(qr_path):
        os.remove(qr_path)

    # Saving the updated state of users and verifications file content
    users_save_data(users)
    save_data(verifications)

    # Finally loggin and display the confirmation of completed deleted process 
    log_event("USER_DELETED", username, "User account deleted")
    print('Account Deleted')
    return True

