# -*- coding: utf-8 -*-

# DB: Fornece uma interface simples para acesso à bancos de dados.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-10-05 
# Modificado em: 2011-10-05 por henriquelima

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import path
from ..base import menu

menus = dict()

def LoadMenu(source):
	menus[source] = menu.Menu(path.MEGAZORD + "/db/" + source, None);

def GetMenu(path):
	if not path in menus:
		LoadMenu(path)
	return menus[path]
