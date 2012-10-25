#!/usr/bin/env python
# -*- coding: utf-8 -*-

# muda_curso: Muda o curso do usuário dado.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-10-24

from supermegazord.db import users
from supermegazord.db import path
from supermegazord.lib import ldapwrap
from supermegazord.lib.account import Account

import sys
if len(sys.argv) != 3:
	print "Uso: %s login novo_curso" % sys.argv[0]
	exit(1)

login = sys.argv[1]
novo_curso = sys.argv[2]
dados = ldapwrap.find_user_by_login(login)

from supermegazord.lib import remote
status_conta = {}
status_conta['mail'] = remote.run_script("mail", "sudo /root/email/rl_atualiza_curso.sh " + login + " " + novo_curso, "megazord")
status_conta['home'] = remote.run_script("nfs", "sudo /megazord/atualiza_curso.sh " + login + " " + novo_curso, "megazord")
status_conta['ldap'] = False

log = open(path.MEGAZORD_DB + "log/uso", "a")
log.write("Mudando curso do usuário '{0}' para '{2}'; Status: {1}\n".format(login, str(status_conta), novo_curso))

for k in status_conta:
	if not status_conta[k]:
		print "Erro: etapa " + k + " mal-sucedida"

