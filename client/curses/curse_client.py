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
    w = 15
    h = len(menu.content)
    color = 2
    
    for x in range(1, w - 1):
        screen.addstr(0, x, '═', curses.color_pair(color))
        screen.addstr(h-1, x, '═', curses.color_pair(color))
        for y in range(1, h-1):
            screen.addstr(y, x, ' ', curses.color_pair(color))
    for y in range(1, h-1):
        screen.addstr(y, 0, '║', curses.color_pair(color))
        screen.addstr(y, w-1, '║', curses.color_pair(color))
    screen.addstr(0, 0, '╔', curses.color_pair(color))
    screen.addstr(0, w-1, '╗', curses.color_pair(color))
    screen.addstr(h-1, 0, '╚', curses.color_pair(color))
    screen.addstr(h-1, w-1, '╝', curses.color_pair(color))
    screen.addstr(0, 4, menu.name, curses.color_pair(color))

megazord = Megazord()

def main(screen):
    global megazord
    PrintMenu(megazord.active_menu, screen)
    while True:
        screen.refresh()

while megazord.Running():
    curses.wrapper(main)
