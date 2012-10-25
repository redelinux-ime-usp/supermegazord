#!/usr/bin/env python
# -*- coding: utf-8 -*-

# desativa_usuario: Desativa a conta do usuário dado
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-10-24

from supermegazord.db import users
from supermegazord.db import path
from supermegazord.lib import ldapwrap
from supermegazord.lib.account import Account

login = sys.argv[1]
dados = ldapwrap.find_user_by_login(login)

from supermegazord.lib import remote
status_conta = {}
status_conta['mail'] = remote.run_script("mail", "sudo /root/email/rl_desativa_login.sh " + login, "megazord")
status_conta['printer'] = remote.run_script("printer", "sudo /root/files/bin/pkdeluser " + login, "megazord")
status_conta['home'] = remote.run_script("nfs", "sudo /megazord/desativa_conta.sh " + login, "megazord")
status_conta['ldap'] = False

log = open(path.MEGAZORD_DB + "log/desativar", "a")
log.write("Desativando usuário '{0}'; Status: {1}\n".format(login, str(status_conta)))

for k in status_conta:
	if not status_conta[k]:
		print "Erro: etapa " + k + " mal-sucedida"

