#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-12-13
# Modificado em: 2011-12-13 por henriquelima

class Menu:
	def __init__(self, data):
		self.name = data["name"]
		self.content = []
		self.lines = []
		self.func = []
		self.data = []
		for line_data in data["content"]:
			name = line_data[0]
			func = None
			arg = None
			
			if line_data[1] == "menu":
				#func = OpenMenu
				arg = line_data[2]
				
			elif line_data[1] == "return":
				#func = ReturnMenu
				arg = None
			
			elif line_data[1] == "shell":
				#func = CallShell
				arg = line_data[2]
				
			elif line_data[1] == "module":
				#func = CallModule
				arg = line_data[2]
				
			self.content.append((name, func, arg))