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

from supermegazord.base.menu import Menu

class Megazord:
    def __init__(self):
        self.menu_dict = {}
        
        tmp = open("D:\stuff\programming\projects\supermegazord\system\megazord.conf", "r")
        self.config = json.load(tmp)
        tmp.close()

        for menu in self.config["menus"]:
            self.menu_dict[menu] = Menu(self.config["menus"][menu])

        self.active_menu = self.menu_dict[self.config["start_menu"]]
