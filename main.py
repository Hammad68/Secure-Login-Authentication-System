from registeration import register
from verification import verify
from accountControl import passord_reset, delete_user
from attackSimulation.dictAttack import execute

if __name__ == '__main__':
    
    while True:

        # Menu to select options
        print('==========================')
        print('1. Register User')
        print('2. Login & Authenticate')
        print('3. Forgot Password')
        print('4. Account Deletion')
        print('5. Dictionary Attack')
        print('6. Exit System')
        print('==========================')
        user_choice = input('Chose Option 1-6: ')
        print('==========================')

        # Processing user selected option
        if user_choice == '1':
            register()
        elif user_choice == '2':
            verify()
        elif user_choice == '3':
            passord_reset()
        elif user_choice == '4':
            delete_user()
        elif user_choice == '5':
            execute()
        else:
            print('Exiting the login system')
            break