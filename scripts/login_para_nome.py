#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
from supermegazord.lib import account

if len(sys.argv) != 2:
	print "Uso: %s login" % sys.argv[0]
	exit(1)

try:
	print account.from_login(sys.argv[1]).name
except:
	print "Usuário desconhecido"
