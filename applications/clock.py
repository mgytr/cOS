from art import *
from datetime import datetime
from time import sleep
from sys import stdin
import sys

from threading import Thread
import tty
import termios

import utils



esc = False
print('\n'*9)

utils.center_print('PRESS Q TO EXIT  ' + datetime.now().strftime('%HH:%MM:%SS'), True, True, False, end='\r')
def clock():
    while not esc:

        utils.center_print('PRESS Q TO EXIT  ' + datetime.now().strftime('%HH:%MM:%SS'), True, False, end='\r')

        sleep(1)
Thread(target=clock).start()


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

while not esc:
    

    if getch() == 'q':
        esc = True

sleep(1)
print()