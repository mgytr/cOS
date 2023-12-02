import json
import threading
from time import sleep
import importlib.util
import sys
import os


processes = []


state = 'running'

def staterefreshthread():
    global state
    print(state)
    while state == 'running':

        state = open('state', 'r').read().strip('\n ')
        print(state)

        sleep(0.5)

    

def refreshthread():
    global processes
    while state == 'running':
        processes = json.load(open('processes.json'))
        sleep(0.6)




def get_processes():
    return json.load(open('processes.json'))

class Process:
    def __init__(self, data) -> None:
        self.name = data['name']
        self.id = data['id']
        self.data = data


def launch_script(path):
    open('state', 'w').write('running')
    spec = importlib.util.spec_from_file_location(path.split('/')[-1].split('.')[0], path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[path.split('/')[-1].split('.')[0]] = foo
    spec.loader.exec_module(foo)
    processes = json.load(open('processes.json'))
    process_id = processes[-1]['id']+1
    data = {'name': path.split('/')[-1].split('.')[0], 'id': process_id}
    processes.append(data)
    open('processes.json', 'w').write(json.dumps(processes))

