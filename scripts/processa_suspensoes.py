#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys, datetime
import supermegazord.lib.account as account
import supermegazord.db.path as path

errfile = path.MEGAZORD_DB + "/log/desativar"

f = None
try:
	if sys.argv[1] == "-":
		f = sys.stdin
	else:
		f = open(sys.argv[1])
except:
	print "Uso: {0} arquivo\nUse '-' para entrada padrão.".format(sys.argv[0])
	sys.exit(1)

users = []
for line in f:
	login = line.strip()
	acc = account.from_login(login)
	if not acc:
		print "Aviso: usuário '{0}' não existe.".format(login)
	else:
		users.append(acc)

f = open(errfile, "a")
f.write("\n{0} -- Processando arquivo {1} com {2} entradas.\n".format(str(datetime.datetime.now()), sys.argv[1], len(users)))
print "Processando {0} contas...".format(len(users))
for acc in users:
	try:
		result = acc.deactivate()
		if not result:
			raise Exception("Deactivate devolveu non-True: " + str(result))
	except Exception, err:
		s = "Erro ao processar '{0}': {1}".format(str(acc), str(err))
		print s
		f.write(s + "\n")
