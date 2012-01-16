# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-12-13
# Modificado em: 2011-12-13 por henriquelima

import functools

class MenuItem:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        
    def HasArgs(self): return False
        
    def Execute(self, args = []):
        return self.func()

class MenuScript:
    def __init__(self, name, script):
        self.name = name
        self.script = script
        
    def HasArgs(self): return True
        
    def Execute(self, args = []):
        return self.script.func(args)
        
class Menu:
    def __init__(self, data, megazord):
        self.name = data["name"].encode("UTF-8")
        self.content = []
        for line_data in data["content"]:
            name = line_data[0].encode("UTF-8")
            item = None

            if line_data[1] == "menu":
                item = MenuItem(name, functools.partial(megazord.OpenMenu, line_data[2]))
            
            elif line_data[1] == "return":
                item = MenuItem(name, megazord.PopMenu)
            
            elif line_data[1] == "script":
                item = MenuScript(name, megazord.scripts[line_data[2]])
            
			#elif line_data[1] == "module":
			#	#func = CallModule
			#	arg = line_data[2]
				
            self.content.append(item)

    def Size(self):
        return len(self.content)
