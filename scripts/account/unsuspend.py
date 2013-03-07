#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

def main(acc):
	import supermegazord.lib.remote as remote
	result = remote.run_script("nfs", "sudo /megazord/scripts/restaurar_conta {0} {1}".format(
													acc.login, acc.group.name), "megazord")
	acc.log("Suspensão removida.")
	if result:
		return "Conta restaurada com successo."
	from supermegazord.lib.tools import ErrorString
	return ErrorString("Erro ao restaurar conta.")

def description():
	return "Restaura a conta."
