

from __future__ import annotations
import colorama
import sys
import typing
from simple_term_menu import *

import urwid
import os


class LineWalker(urwid.ListWalker):

    def __init__(self, name):
        self.file = open(name)  
        self.lines = []
        self.focus = 0

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start_from):
        return self._get_at_pos(start_from + 1)

    def get_prev(self, start_from):
        return self._get_at_pos(start_from - 1)

    def read_next_line(self):

        next_line = self.file.readline()

        if not next_line or next_line[-1:] != '\n':
            
            self.file = None
        else:
            
            next_line = next_line[:-1]

        expanded = next_line.expandtabs()

        edit = urwid.Edit('', expanded, allow_tab=True)
        edit.set_edit_pos(0)
        edit.original_text = next_line
        self.lines.append(edit)

        return next_line

    def _get_at_pos(self, pos):

        if pos < 0:
            
            return None, None

        if len(self.lines) > pos:
            
            return self.lines[pos], pos

        if self.file is None:
            
            return None, None

        assert pos == len(self.lines), 'out of order request?'  

        self.read_next_line()

        return self.lines[-1], pos

    def split_focus(self):


        focus = self.lines[self.focus]
        pos = focus.edit_pos
        edit = urwid.Edit('', focus.edit_text[pos:], allow_tab=True)
        edit.original_text = ''
        focus.set_edit_text(focus.edit_text[:pos])
        edit.set_edit_pos(0)
        self.lines.insert(self.focus + 1, edit)

    def combine_focus_with_prev(self):


        above, ignore = self.get_prev(self.focus)
        if above is None:
            
            return

        focus = self.lines[self.focus]
        above.set_edit_pos(len(above.edit_text))
        above.set_edit_text(above.edit_text + focus.edit_text)
        del self.lines[self.focus]
        self.focus -= 1

    def combine_focus_with_next(self):


        below, ignore = self.get_next(self.focus)
        if below is None:
            
            return

        focus = self.lines[self.focus]
        focus.set_edit_text(focus.edit_text + below.edit_text)
        del self.lines[self.focus + 1]


class EditDisplay:
    palette: typing.ClassVar[list[tuple[str, str, str, ...]]] = [
        ('body', 'default', 'default'),
        ('foot', 'white', 'dark green', 'bold'),
        ('key', 'white', 'dark green', 'underline'),
    ]

    footer_text = (
        'foot',
        [
            ('key', 'F5'),
            '  save and quit   ',
            ('key', 'F6'),
            '  quit without saving   '
        ],
    )

    def __init__(self, name):
        self.save_name = name
        self.walker = LineWalker(name)
        self.listbox = urwid.ListBox(self.walker)
        self.footer = urwid.AttrMap(urwid.Text(self.footer_text), 'foot')
        self.view = urwid.Frame(urwid.AttrMap(self.listbox, 'body'), footer=self.footer)

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.unhandled_keypress)
        self.loop.run()

    def unhandled_keypress(self, k):


        if k == 'f5':
            self.save_file()
            raise urwid.ExitMainLoop()
        elif k == 'f6':
            raise urwid.ExitMainLoop()
        elif k == 'delete':
            
            self.walker.combine_focus_with_next()
        elif k == 'backspace':
            
            self.walker.combine_focus_with_prev()
        elif k == 'enter':
            
            self.walker.split_focus()
            
            self.loop.process_input(['down', 'home'])
        elif k == 'right':
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_next(pos)
            if w:
                self.listbox.set_focus(pos, 'above')
                self.loop.process_input(['home'])
        elif k == 'left':
            w, pos = self.walker.get_focus()
            w, pos = self.walker.get_prev(pos)
            if w:
                self.listbox.set_focus(pos, 'below')
                self.loop.process_input(['end'])
        else:
            return None
        return True

    def save_file(self):
        lines = []
        walk = self.walker
        for edit in walk.lines:
            
            if edit.original_text.expandtabs() == edit.edit_text:
                lines.append(edit.original_text)
            else:
                lines.append(re_tab(edit.edit_text))

        
        while walk.file is not None:
            lines.append(walk.read_next_line())

        
        with open(self.save_name, 'w') as outfile:
            prefix = ''
            for line in lines:
                outfile.write(prefix + line)
                prefix = '\n'


def re_tab(s):
    line = []
    p = 0
    for i in range(8, len(s), 8):
        if s[i - 2 : i] == '  ':
            
            line.append(f'{s[p:i].rstrip()}\t')
            p = i

    if p == 0:
        return s

    line.append(s[p:])
    return ''.join(line)


def main():

    while 1:
        os.system('clear')   
        options: list = os.listdir(f'users/{open("activeuser").read()}/Personal Files')
        options.insert(0, '/Create a New File/')
        options.insert(1, '/Delete a File/')
        options.insert(2, '/Refresh/')
        options.insert(3, '/Abort/')
        menu = TerminalMenu(options, title='Files')
        menu_entry_index = menu.show()
        selected: str = options[menu_entry_index]
        if selected.startswith('/'):
            if selected == '/Create a New File/':
                while 1:
                    nameinp = input(f'{colorama.Fore.GREEN}Enter your file name>>{colorama.Fore.RESET} ')
                    if any(i in '/\0\\' for i in nameinp):
                        print(f'{colorama.Fore.RED}FATAL:{colorama.Fore.RESET} The filename should not contain slashes (/), null (\\0) and backslashes (\\)')
                    elif os.path.exists(f'users{open("activeuser").read()}/Personal Files/' + nameinp):
                        print(f'{colorama.Fore.RED}FATAL:{colorama.Fore.RESET} This file already exists!')
                    else:
                        break
                open(f'users/{open("activeuser").read()}/Personal Files/' + nameinp, 'w+').write('')
            elif selected == '/Abort/':
                return
            elif selected == '/Delete a File/':
                while 1:
                    options: list = os.listdir(f'users/{open("activeuser").read()}/Personal Files')
                    options.insert(0, '/Abort/')
                    menu = TerminalMenu(options, title='Delete a File')
                    menu_entry_index = menu.show()
                    selected: str = options[menu_entry_index]
                    if selected.startswith('/'):
                        break
                    else:
                        options = ['Yes', 'No']
                        menu = TerminalMenu(options, title=f'Are you sure you want to delete "{selected}"?')
                        index = menu.show()
                        if options[index] == 'Yes':
                            os.remove(f'users/{open("activeuser").read()}/Personal Files/{selected}')
                            break
                        






        else:
            name = f'users/{open("activeuser").read()}/Personal Files/' + selected
            break


            

    print(name)
    try:
        assert open(name, 'a')
    except (FileNotFoundError, OSError):
        sys.stderr.write(__doc__)
        return
    EditDisplay(name).main()


main()