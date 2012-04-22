# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-01-15
# Modificado em: 2012-04-22 por henriquelima

import subprocess, functools
from supermegazord.db import path

def ScriptSubprocess(path, args = []):
    command = path
    for arg in args:
        command = command + " " + arg
    subprocess.call(command, shell=True)
    #print command

class ScriptArg:
    def __init__(self, data):
        try:    self.description = data["description"].encode("UTF-8")
        except: self.description = "Sem descrição".encode("UTF-8")
                
        try:    self.default  = data["default"].encode("UTF-8")
        except: self.default  = "";
                
        try:    self.prefix = data["prefix"].encode("UTF-8")
        except: self.prefix = ""
        
    def Parse(self, input):
        resp = input
        if input == "":
            resp = self.default
        
        return self.prefix + resp
    
class Script:
    def __init__(self, data, megazord):
        self.func = lambda args = []: False
        self.disable_curses = False
        
        # Simple "execute a file"
        if data["type"] == "shell":
            self.disable_curses = True
            spath = data["path"].encode("UTF-8").replace("{MEGAZORD}", path.MEGAZORD)
            self.func = functools.partial(ScriptSubprocess, spath)
            self.args = []
            if "args" in data:
                for arg in data["args"]:
                    self.args.append(ScriptArg(arg))
