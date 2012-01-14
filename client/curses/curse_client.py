#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05
# Modificado em: 2011-08-05 por henriquelima

import sys
sys.path.append("/root/")

if __name__ != "__main__":
    print "Esse script é interativo e não um módulo."
    quit()

# Megazord global variables
from supermegazord.system.megazord import Megazord
megazord = Megazord()
current_line = 0

import curses
# Curses global variables
curses_quit = False
from supermegazord.base import colors

def PrintMenu(menu, screen, offset_y = 0, offset_x = 0):
    w = 40
    h = len(menu.content) + 2
    color = 2
    
    for x in range(1, w - 1):
        screen.addstr(offset_y +    0 , offset_x + x, '═')
        screen.addstr(offset_y + (h-1), offset_x + x, '═')
        for y in range(1, h-1):
            screen.addstr(offset_y + y, offset_x + x, ' ')
    for y in range(1, h-1):
        screen.addstr(offset_y + y, offset_x +   0  , '║')
        screen.addstr(offset_y + y, offset_x + (w-1), '║')
    screen.addstr(offset_y +   0  , offset_x +   0  , '╔')
    screen.addstr(offset_y +   0  , offset_x + (w-1), '╗')
    screen.addstr(offset_y + (h-1), offset_x +   0  , '╚')
    screen.addstr(offset_y + (h-1), offset_x + (w-1), '╝')
    screen.addstr(offset_y +   0  , offset_x +   4  , menu.name)

    global megazord, current_line
    for i in range(0, len(menu.content)):
        if current_line == i and menu == megazord.active_menu:
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
       

def main(screen):
    #screen.nodelay(True)
    global megazord, current_line
    colors.init()

    global curses_quit
    curses_quit = False
    while megazord.Running() and not curses_quit:
        screen.clear()
        PrintMenuList(screen)
        c = screen.getch()
        if c == ord('q'):
            megazord.Quit()
        elif c == curses.KEY_DOWN or c == ord('2'):
            current_line = (current_line + 1) % megazord.active_menu.Size()
        elif c == curses.KEY_UP or c == ord('1'):
            current_line = (current_line - 1) % megazord.active_menu.Size()
        elif c == ord('\n'):
            megazord.ExecuteLine(current_line)
            current_line = 0
        else:
            screen.refresh()

while megazord.Running():
    curses.wrapper(main)
