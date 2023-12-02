import kernel



def init():

    open('processes.json', 'w').write('''[
        {"name": "Kernel", "id": -1}
]''')

    kernel.threading.Thread(target=kernel.refreshthread).start()
    kernel.launch_script('system/init.py')








