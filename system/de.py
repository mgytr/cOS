import sys

import colorama, launch, json, os

from simple_term_menu import *



def launch_de(username):
    while 1:
        os.system('clear')
        data: dict = json.load(open('applications/maps.json'))
        
        options = [x for x in data.keys()]
        options.append('Log off')
        options.append('Shut down')

        terminal_menu = TerminalMenu(options, title='Programs', quit_keys=tuple())
        menu_entry_index = terminal_menu.show()
        selected = options[menu_entry_index]
        os.system('clear')

        if menu_entry_index == len(options)-1 or menu_entry_index == len(options)-2:

            if menu_entry_index == len(options)-2:
                return
            else:
                open('state', 'w').write('stopped')
                os._exit(0)
                
        else:
            launch.launch_script('applications/' + data[selected])
        

        
        