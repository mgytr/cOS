
import sys
import os
import time

print('Init stage!')
time.sleep(2)

sys.path.append('system')

os.system('clear')
time.sleep(3)
import launch

launch.launch_script('system/logincli.py')