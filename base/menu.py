#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-12-13
# Modificado em: 2011-12-13 por henriquelima

class Menu:
	def __init__(self, path):
		source = open(path, 'r')
		self.name = source.readline().replace('\n', '')
		self.lines = []
		self.func = []
		self.data = []
		for line in source:
			line_data = line.replace('\n','').split(':', 2)
			self.lines.append(line_data[0])
			if line_data[1] == "menu":
				self.data.append(line_data[2])
				#self.func.append(OpenMenu)
			elif line_data[1] == "return":
				self.data.append(None)
				#self.func.append(ReturnMenu)
			elif line_data[1] == "shell":
				self.data.append(line_data[2])
				#self.func.append(CallShell)
			elif line_data[1] == "module":
				self.data.append(line_data[2])
				#self.func.append(CallModule)

	def AddLine(self, line):
		self.lines.append(line)