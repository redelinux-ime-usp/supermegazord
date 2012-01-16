#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-12-13
# Modificado em: 2011-12-13 por henriquelima

import sys
sys.path.append("/root/")

if __name__ != "__main__":
    print "Esse script é interativo e não um módulo."
    quit()

from supermegazord.system.megazord import Megazord


def PrintMenu(menu):
    print "=============="
    print menu.name
    for i in range(len(menu.content)):
        print str(i) + ": " + menu.content[i].name
    print


megazord = Megazord()
current_menu = None
while megazord.Running():
    if current_menu != megazord.active_menu:
        current_menu = megazord.active_menu
        PrintMenu(current_menu)
    
    command = raw_input("> ")
    if command == "quit" or command == "q" or command == "sair":
        megazord.Quit()
    elif command == "menu":
        PrintMenu(current_menu)
    elif command == "help" or command == "ajuda":
        print "Comandos: q/quit/sair, menu, help/ajuda"
    elif command != "":
        line = -1
        try:
            line = int(command)
        except:
            print "Comando desconhecido."
        if line != -1:
            menu_line = megazord.CurrentLine(line)
            if not menu_line.HasArgs():
                menu_line.Execute(line)
            else:
                args = []
                for script_arg in menu_line.script.args:
                    if script_arg.default != "":
                        default_value = "[" + script_arg.default + "] "
                    else:
                        default_value = ""
                    
                    user_arg_input = raw_input(script_arg.description + ": " + default_value)
                    args.append(script_arg.Parse(user_arg_input))
                menu_line.Execute(args)
