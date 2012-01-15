#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-01-15
# Modificado em: 2012-01-15 por henriquelima

import subprocess, functools, sys

def ScriptSubprocess(path):
    subprocess.call(path, shell=True, stdin=sys.stdin, stdout=sys.stdout)

class Script:
    def __init__(self, data, megazord):
        self.func = lambda: False
        self.disable_curses = False
        
        # Simple "execute a file"
        if data["type"] == "shell":
            self.disable_curses = True
            self.func = functools.partial(ScriptSubprocess, data["path"])
            
