#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

def main(acc):
	import supermegazord.lib.remote as remote
	result = remote.run_script("nfs", "sudo /megazord/scripts/suspende_conta {0} {1}".format(
													acc.login, acc.group.name), "megazord")
	acc.log("Conta suspensa.")
	if result:
		return "Conta suspensa com successo."
	from supermegazord.lib.tools import ErrorString
	return ErrorString("Erro ao suspender conta.")

def description():
	return "Suspende a conta."
