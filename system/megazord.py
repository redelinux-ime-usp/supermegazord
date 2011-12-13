#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-12-13
# Modificado em: 2011-12-13 por henriquelima

import sys
sys.path.append("D:\\stuff\\programming\\projects")

import ConfigParser 

from supermegazord.base.menu import Menu

class Megazord:
    def __init__(self):
        self.menu_list = []
        self.config = ConfigParser.ConfigParser()
        self.config.read("D:\stuff\programming\projects\supermegazord\system\megazord.conf")
