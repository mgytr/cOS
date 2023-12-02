import os
import getpass
import colorama
import hashlib
import json
import launch

colorama.init()
open('activeuser', 'w').write('ß')
def login():
    if not os.path.exists('users'):
        os.mkdir('users')
    
    users = os.listdir('users')

    if len(users) == 0:
        print(f'{colorama.Fore.RED}FATAL:{colorama.Fore.RESET} There are no users!')
        while 1:
            username = input(f'{colorama.Fore.GREEN}Choose your username>>{colorama.Fore.RESET} ')
            if username and set(username).issubset(set('qwertyuiopasdfghjklzxcvbnm1234567890')):
                break
            else:
                print(f'{colorama.Fore.RED}ERROR:{colorama.Fore.RESET} Your username can only contain latin letters (a-z) and numbers')
        password_hash = hashlib.sha256(getpass.getpass(f'{colorama.Fore.GREEN}Choose your password>>{colorama.Fore.RESET} ').encode()).hexdigest()

        users = json.load(open('system/uapd.json'))
        users[username] = password_hash
        open('system/uapd.json', 'w').write(json.dumps(users))
        os.mkdir(f'users/{username}')
        os.mkdir(f'users/{username}/Personal Files')
        os.mkdir(f'users/{username}/Options')
        login()
    else:

        while 1:
            print('Please enter your credentials.')
            print(f'The users are: {", ".join(os.listdir("users"))}')
            username = input(f'{colorama.Fore.GREEN}Enter your username>>{colorama.Fore.RESET} ')
            if username in os.listdir('users'):
                pass
            else:
                print(f'{colorama.Fore.RED}FATAL:{colorama.Fore.RESET} This user does not exist.')
                continue
        
            password_hash = hashlib.sha256(getpass.getpass(f'{colorama.Fore.GREEN}Enter your password>>{colorama.Fore.RESET} ').encode()).hexdigest()
            if json.load(open('system/uapd.json'))[username] == password_hash:
                open('activeuser', 'w').write(username)
                launch.launch_script('system/de.py', 'launch_de', {'username': username})
                



            



login()