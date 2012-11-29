#!/usr/bin/env python
# -*- coding: utf-8 -*-

# desativa_usuario: Desativa a conta do usuário dado
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-10-24

from supermegazord.db import users
from supermegazord.db import path
from supermegazord.lib import remote
import supermegazord.lib.account as account

import sys
if len(sys.argv) != 2:
	print "Uso: %s login" % sys.argv[0]
	exit(1)

user = account.from_login(sys.argv[1])

if not user:
	print "Usuário inválido."
	exit(1)

def comando(user):
	return "sudo /megazord/scripts/desativa_conta " + user.login + " " + user.group.name
	
to_run = ['mail', 'printer', 'home', 'ldap']
commands = {
	'mail':    lambda user: remote.run_script("mail",    comando(user), "megazord") == 0,
	'printer': lambda user: remote.run_script("printer", comando(user), "megazord") == 0,
	'home':    lambda user: remote.run_script("home",    comando(user), "megazord") == 0,
	'ldap':    lambda user: False
}

status_conta = {}
for running in to_run:
	print "\nDesativando do {0}...".format(running)
	status_conta[running] = commands[running](user)

log = open(path.MEGAZORD_DB + "log/desativar", "a")
log.write("Desativando usuário '{0}'; Status: {1}\n".format(user.login, str(status_conta)))

for k in status_conta:
	if not status_conta[k]:
		print "Erro: etapa '" + k + "' mal-sucedida"

