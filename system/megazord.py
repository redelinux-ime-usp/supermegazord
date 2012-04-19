# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-12-13
# Modificado em: 2012-01-15 por henriquelima

import json
import subprocess

from supermegazord.base.menu import Menu
from supermegazord.base.script import Script
from supermegazord.db import path
 
# Evento de saída: active_menu == None

class Megazord:
    def __init__(self):
        tmp = open(path.MEGAZORD + "system/megazord.conf", "r")
        self.config = json.load(tmp)
        tmp.close()
        
        self.scripts = {}
        for script in self.config["scripts"]:
            self.scripts[script] = Script(self.config["scripts"][script], self)
            

        self.menus = {}
        for menu in self.config["menus"]:
            self.menus[menu] = Menu(self.config["menus"][menu], self)

        self.active_menu = self.menus[self.config["start_menu"]]
        self.menu_history = []

    def Quit(self):
        self.active_menu = None
        self.menu_history = []

    def Running(self):
        return self.active_menu != None
        
    def OpenMenu(self, menu):
        next_menu = None
        try:
            next_menu = self.menus[menu]
        except:
            print "Erro Interno: Menu desconhecido."
            
        if next_menu != None:
            self.menu_history.append(self.active_menu)
            self.active_menu = next_menu
        
    def PopMenu(self):
        try: # Volta pro menu anterior
            self.active_menu = self.menu_history.pop()
        except: # Sai do programa
            self.active_menu = None
            
    def CurrentLine(self, line):
        try:
            return self.active_menu.content[line]
        except:
            return None

    def ExecuteLine(self, line):
        command = self.CurrentLine(line)
        if command != None:
            return command.Execute()
        return False
