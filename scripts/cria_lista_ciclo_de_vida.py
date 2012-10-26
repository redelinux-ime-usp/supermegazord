#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import supermegazord.lib.ldapwrap as ldapwrap
import supermegazord.db.path as path

nidsok = {}
with open(path.MEGAZORD_DB + "usuarios/jupiter/jup_info", "r") as jupinfo:
	for line in jupinfo:
		nidsok[line.split(':')[0]] = True
	
with open(path.MEGAZORD_DB + "usuarios/jupiter/nojup_info", "r") as nojupinfo:
	for line in nojupinfo:
		nidsok[line.split(':')[0]] = True


IMORTAIS = ldapwrap.find_grupo_by_name('imortais')
users = ldapwrap.query("ou=People")

for u in users:
	if 'nid' in u[1]:
		if u[1]['nid'][0] not in nidsok and u[1]['uid'][0] not in IMORTAIS['memberUid']:
			print u[1]['uid'][0]

