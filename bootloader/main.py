import sys
sys.path.append('kernel')
sys.path.append('uiutils')
import os
import utils
import time








utils.center_print('''          ____     _____ 
         / __ \   / ____|
   ___  | |  | | | (___  
  / __| | |  | |  \___ \ 
 | (__  | |__| |  ____) |
 \___|  \____/  |_____/
                     ''', True, True)




time.sleep(2)
utils.center_print('Loading kernel', True, False)

import init_kernel
init_kernel.init()

time.sleep(2)

thr = init_kernel.kernel.threading.Thread(target=init_kernel.kernel.staterefreshthread)
thr.start()
thr.join()
