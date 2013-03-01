#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys, time, datetime
import supermegazord.lib.account as account
import supermegazord.db.path as path
from progressbar import ProgressBar, Counter, Timer

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

data = f.read().strip().split('\n')
users = []

pbar = ProgressBar(widgets=['Processed: ', Counter(), ' lines (', Timer(), ')'], maxval=len(data))
pbar.start()
for line in data:
	login = line.strip()
	acc = account.from_login(login)
	if not acc:
		print "Aviso: usuário '{0}' não existe.".format(login)
	else:
		users.append(acc)
	pbar.update(len(users))
pbar.finish()

f = open(errfile, "a")
f.write("\n{0} -- Processando arquivo {1} com {2} entradas.\n".format(str(datetime.datetime.now()), sys.argv[1], len(users)))
print "Processando {0} contas...".format(len(users))
start = time.time()
for acc in users:
	userstart = time.time()
	print "> User: {0}".format(acc.login)
	try:
		result = acc.run_script("deactivate")
		if not result:
			raise Exception("Deactivate devolveu non-True: " + str(result))
	except Exception, err:
		s = "Erro ao processar '{0}': {1}".format(str(acc), str(err))
		print s
		f.write(s + "\n")
	print "-- Done in {0}".format(time.time() - userstart)
elapsed = time.time() - start
print "Fim. Tempo gasto: " + str(elapsed)
f.write("-- Tempo Gasto: {0}\n".format(elapsed))
