#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

def main(self):
	from supermegazord.lib import remote, kerbwrap, ldapwrap, account
	command = "sudo /megazord/scripts/apaga_conta " + self.login + " " + self.group.name
	results = remote.run_remote_batch(['mail', 'printer', 'nfs'], command, "megazord")
	for s in results: results[s] = (results[s] == 0)
	results['kerberos'] = kerbwrap.delete_user(self.login) == 0
	results['ldap'] = ldapwrap.delete_user(self.login)
	del account.cache[self.uid]
	self.log("Conta '{0}' removida. Status: {1}".format(self.login, str(results)))
	if not reduce(lambda a, b: a and b, results.values()):
		return False
	else:
		return "Conta '{0}' removida com sucesso.".format(self.login)

def description():
	return "Remove a conta completamente."
