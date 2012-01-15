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
import functools

# Cria e inicializa o nosso megazord
megazord = Megazord()

# Memoriza a linha atual de cada menu
current_line = dict()
current_line[megazord.active_menu] = 0

# Quando o curses reinicia, se essa variavel é != None, ela´é executada como uma função
queued_execution = None

import curses, curses.textpad
# Curses global variables
curses_quit = False
from supermegazord.base import colors

def DrawBorders(screen, offset_y, offset_x, h, w, title = ""):
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
    try:
        screen.addstr(offset_y + (h-1), offset_x + (w-1), '╝')
    except curses.error: pass
    if title != "":
        screen.addstr(offset_y +   0  , offset_x +   4  , title)



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
    return win.getstr(2 + i*2, 2, 40)
    
 
def GetInput(screen, script_args):
    win = curses.newwin((len(script_args) + 1) * 2, 45, 3, 20)
    win.clear()
    DrawBorders(win, 0, 0, (len(script_args) + 1) * 2, 45)
    #win.border()
    curses.curs_set(1)
    curses.echo()
    resp = []
    for i in range(0, len(script_args)):
        resp.append(GetInputSingle(win, i, script_args[i]))
    curses.curs_set(0)
    curses.noecho()
    return resp

def main(screen):
    #screen.nodelay(True)
    curses.curs_set(0)

    global megazord, current_line
    colors.init()

    global curses_quit
    curses_quit = False
    redraw = True
    while megazord.Running() and not curses_quit:
        if redraw:
            screen.clear()
            PrintMenuList(screen)
            redraw = False
        c = screen.getch()
        if c == ord('q'):
            megazord.Quit()
        elif c == curses.KEY_DOWN or c == ord('2'):
            current_line[megazord.active_menu] = (current_line[megazord.active_menu] + 1) % megazord.active_menu.Size()
            redraw = True
        elif c == curses.KEY_UP or c == ord('1'):
            current_line[megazord.active_menu] = (current_line[megazord.active_menu] - 1) % megazord.active_menu.Size()
            redraw = True
        elif c == curses.KEY_LEFT:
            megazord.PopMenu()
            redraw = True
        elif c == curses.KEY_END:
            current_line[megazord.active_menu] = megazord.active_menu.Size() - 1
            redraw = True
        elif c == curses.KEY_HOME:
            current_line[megazord.active_menu] = 0
            redraw = True
        elif c == ord('\n'):
            menu_line = megazord.CurrentLine(current_line[megazord.active_menu])
            global queued_execution
            if not menu_line.HasArgs():
                queued_execution = menu_line.Execute
            else:
                args = GetInput(screen, menu_line.script.args)
                queued_execution = functools.partial(menu_line.Execute, args)
            curses_quit = True
        else:
            screen.refresh()

while megazord.Running():
    if queued_execution != None:
        menu_count = len(megazord.menu_history)
        queued_execution()
        if megazord.active_menu not in current_line or menu_count < len(megazord.menu_history):
            current_line[megazord.active_menu] = 0
        queued_execution = None
    curses.wrapper(main)
