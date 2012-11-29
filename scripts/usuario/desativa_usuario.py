#!/usr/bin/env python
# -*- coding: utf-8 -*-

# desativa_usuario: Desativa a conta do usuário dado
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-10-24

from supermegazord.db import users
from supermegazord.db import path
from supermegazord.lib import ldapwrap
from supermegazord.lib.account import Account

import sys
if len(sys.argv) != 2:
	print "Uso: %s login" % sys.argv[0]
	exit(1)

login = sys.argv[1]
dados = ldapwrap.find_user_by_login(login)

if not dados:
	print "Usuário inválido."
	exit(1)

group = ldapwrap.find_group_by_gid(dados['gidNumber'][0])['cn'][0]

from supermegazord.lib import remote
status_conta = {}

comando = "sudo /megazord/scripts/desativa_conta " + login + " " + group

print "Desativando do mail..."
status_conta['mail']    = remote.run_script("mail",    comando, "megazord") == 0

print "\nDesativando do printer..."
status_conta['printer'] = remote.run_script("printer", comando, "megazord") == 0

print "\nDesativando do NFS..."
status_conta['home']    = remote.run_script("nfs",     comando, "megazord") == 0

print "\nDesativando do LDAP..."
print "Não implementado...\n"
status_conta['ldap'] = False

log = open(path.MEGAZORD_DB + "log/desativar", "a")
log.write("Desativando usuário '{0}'; Status: {1}\n".format(login, str(status_conta)))

for k in status_conta:
	if not status_conta[k]:
		print "Erro: etapa " + k + " mal-sucedida"

