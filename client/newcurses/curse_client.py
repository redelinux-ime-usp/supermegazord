#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05
# Modificado em: 2011-08-05 por henriquelima

# Megazord global variables
from supermegazord.system.megazord import Megazord
import functools

quit = False

# Memoriza a linha atual de cada menu
current_line = 0

# Lista atual de usuarios
user_list = list()

import curses, curses.textpad
# Curses global variables
curses_quit = False
from supermegazord.base import colors

def PrintUsers(screen, start, count, offset_y, offset_x):
    start = max(start, 0)
    for i in range(start, min(start+count, len(user_list))):
        if i == current_line:
            screen.addstr(offset_y + i - start, offset_x, user_list[i].login, colors.YELLOW)
        else:
            screen.addstr(offset_y + i - start, offset_x, user_list[i].login)

def DrawBorders(screen, offset_y, offset_x, h, w, title = ""):
    BORDER_TOP          = u'═'.encode('UTF-8')
    BORDER_BOTTOM       = u'═'.encode('UTF-8')
    BORDER_LEFT         = u'║'.encode('UTF-8')
    BORDER_RIGHT        = u'║'.encode('UTF-8')
    BORDER_TOP_LEFT     = u'╔'.encode('UTF-8')
    BORDER_TOP_RIGHT    = u'╗'.encode('UTF-8')
    BORDER_BOTTOM_LEFT  = u'╚'.encode('UTF-8')
    BORDER_BOTTOM_RIGHT = u'╝'.encode('UTF-8')
    try:
        for x in range(1, w - 1):
            screen.addstr(offset_y +    0 , offset_x + x, BORDER_TOP)
            screen.addstr(offset_y + (h-1), offset_x + x, BORDER_BOTTOM)
            for y in range(1, h-1):
                screen.addstr(offset_y + y, offset_x + x, ' ')
        for y in range(1, h-1):
            screen.addstr(offset_y + y, offset_x +   0  , BORDER_LEFT)
            screen.addstr(offset_y + y, offset_x + (w-1), BORDER_RIGHT)
        screen.addstr(offset_y +   0  , offset_x +   0  , BORDER_TOP_LEFT)
        screen.addstr(offset_y +   0  , offset_x + (w-1), BORDER_TOP_RIGHT)
        screen.addstr(offset_y + (h-1), offset_x +   0  , BORDER_BOTTOM_LEFT)
        screen.addstr(offset_y + (h-1), offset_x + (w-1), BORDER_BOTTOM_RIGHT)
        if title != "":
            screen.addstr(offset_y +   0  , offset_x +   4  , title)
    except curses.error:
        pass

def PrintMenu(menu, screen, offset_y = 0, offset_x = 0):
    w = 40
    h = len(menu.content) + 2
    color = 2
    
    DrawBorders(screen, offset_y, offset_x, h, w, menu.name)

    global megazord, current_line
    for i in range(0, len(menu.content)):
        # Santas variáveis globais batman
        if current_line[menu] == i:# and menu == megazord.active_menu:
            screen.addstr(offset_y + i + 1, offset_x + 2, menu.content[i].name, colors.YELLOW)
        else:
            screen.addstr(offset_y + i + 1, offset_x + 2, menu.content[i].name)
        
def PrintMenuList(screen):
    global megazord
    menu_list = [megazord.active_menu]
    for menu in megazord.menu_history:
        menu_list.append(menu)
    
    num_menu = len(menu_list)
    for i in range(num_menu - 1, -1, -1):
        PrintMenu(menu_list[i], screen, num_menu - i, num_menu - i)

def GetInputSingle(win, i, script_arg):
    if script_arg.default != "":
        default_value = "[" + script_arg.default + "] "
    else:
        default_value = ""

    win.addstr(1 + i*2, 3, script_arg.description + " " + default_value)
    win.refresh()
    return script_arg.Parse(win.getstr(2 + i*2, 2, 40))
    
def main(screen):
    #screen.nodelay(True)
    curses.curs_set(0)

    global quit, current_line
    colors.init()

    redraw = True
    while not quit:
        if redraw:
            screen.clear()
            PrintUsers(screen, current_line - 10, 20, 1, 1)
            redraw = False
        c = screen.getch()
        if c == ord('q'):
            quit = True
        elif c == ord('/'):
            pass
        elif c == curses.KEY_DOWN or c == ord('2'):
            current_line = current_line + 1
            redraw = True
        elif c == curses.KEY_UP or c == ord('1'):
            current_line = current_line - 1
            redraw = True
        elif c == curses.KEY_LEFT:
            redraw = True
        elif c == curses.KEY_END:
            redraw = True
        elif c == curses.KEY_HOME:
            redraw = True
        elif c == ord('\n'):
            pass
        else:
            screen.refresh()

def Run():
    import supermegazord.lib.account as account
    global user_list
    user_list = sorted(account.search(""), key=lambda item: item.login)
    curses.wrapper(main)

if __name__ == "__main__":
    Run()
