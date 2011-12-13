#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-12-13
# Modificado em: 2011-12-13 por henriquelima

import sys
sys.path.append("D:\\stuff\\programming\\projects")

import json
import subprocess

from supermegazord.base.menu import Menu

# Evento de quit: active_menu == None

class Megazord:
    def __init__(self):
        tmp = open("D:\stuff\programming\projects\supermegazord\system\megazord.conf", "r")
        self.config = json.load(tmp)
        tmp.close()

        self.menus = {}
        for menu in self.config["menus"]:
            self.menus[menu] = Menu(self.config["menus"][menu])

        self.active_menu = self.menus[self.config["start_menu"]]
        self.menu_history = []

    def Quit(self):
        self.active_menu = None
        self.menu_history = []

    def Running(self):
        return self.active_menu != None

    def ExecuteLine(self, line):
        if line >= len(self.active_menu.content):
            return False

        command = self.active_menu.content[line]
        if command.func == "menu" or command.func == "return":
            next_menu = None
            if command.func == "menu":
                self.menu_history.append(self.active_menu)
                next_menu = self.menus[command.arg]
            elif len(self.menu_history) > 0:
                next_menu = self.menu_history.pop()
            self.active_menu = next_menu

        elif command.func == "shell":
            subprocess.call(command.arg, shell=True,
                                         stdin=sys.stdin,
					 stdout=sys.stdout)

        return True
