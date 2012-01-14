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
    print __name__
    quit()

from supermegazord.system.megazord import Megazord

import curses

def PrintMenu(menu, screen):
    w = 20
    h = len(menu.content) + 2
    color = 2
    offset_x = 0
    offset_y = 0
    
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

    for i in range(0, len(menu.content)):
        screen.addstr(offset_y + i + 1, offset_x + 2, menu.content[i].name)
        

megazord = Megazord()

curses_quit = False

def main(screen):
    #screen.nodelay(True)
    global megazord
    PrintMenu(megazord.active_menu, screen)

    global curses_quit
    curses_quit = False
    while megazord.Running() and not curses_quit:
        c = screen.getch()
        if c == ord('q'):
            megazord.Quit()
        else:
            screen.refresh()

while megazord.Running():
    curses.wrapper(main)
