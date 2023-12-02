import os
def center_print(s: str, x: bool, y: bool, y_down=True, end='\n'):
    width, height = os.get_terminal_size().columns, os.get_terminal_size().lines
    lines = s.splitlines()
    if y:
        print('\n'*(int(height/2)-int(len(lines)/2)))
    for i in lines[:-1]:
        i: str


        print(i.center(width))
    print(lines[-1].center(width), end=end)
    if y and y_down:
        print('\n'*(int(height/2)-int(len(lines)/2)))
