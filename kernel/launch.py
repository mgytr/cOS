import threading
import sys
import json
import importlib


def launch_script(path, call=None, callargs={}):
    open('state', 'w').write('running')
    spec = importlib.util.spec_from_file_location(path.split('/')[-1].split('.')[0], path)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[path.split('/')[-1].split('.')[0]] = foo

    
    processes = json.load(open('processes.json'))
    process_id = processes[-1]['id']+1
    data = {'name': path.split('/')[-1].split('.')[0], 'id': process_id}
    processes.append(data)
    open('processes.json', 'w').write(json.dumps(processes))
    spec.loader.exec_module(foo)
    
    if call != None:
        getattr(foo, call)(**callargs)
