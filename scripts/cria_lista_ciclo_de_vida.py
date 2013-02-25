#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import supermegazord.lib.account as account
import supermegazord.lib.group as group
import supermegazord.db.path as path

juppath = path.MEGAZORD_DB + "usuarios/jupiter/jup_info"
if len(sys.argv) > 1:
	juppath = sys.argv[1]

nidsok = {}
with open(juppath, "r") as jupinfo:
	for line in jupinfo:
		nidsok[line.split(':')[0]] = True
	
with open(path.MEGAZORD_DB + "usuarios/jupiter/nojup_info", "r") as nojupinfo:
	for line in nojupinfo:
		nidsok[line.split(':')[0]] = True


IMORTAIS = group.from_name('imortais')
EXALUNO = group.from_name('exaluno')
users = account.search("")

for u in users:
	if u.nid not in nidsok and u.group != EXALUNO and u.login not in IMORTAIS.members:
		print u.login

