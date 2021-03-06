# -*- coding: utf-8 -*-

def main(self):
	if self.group.name == "exaluno": return "Conta já inativa."
	from supermegazord.lib.tools import ErrorString
	import supermegazord.db.path as path
	try:
		with open(path.MEGAZORD_DB + "/emails/account.deactivate") as f:
			self.mail("Conta Desativada", f.read().format(**self.__dict__))
	except: pass
	import supermegazord.lib.remote as remote
	command = "sudo /megazord/scripts/desativa_conta " + self.login + " " + self.group.name
	results = remote.run_remote_batch(['mail', 'printer', 'nfs'], command, "megazord")
	results['ldap'] = self.group.add_member(self) and self.change_group('exaluno') and (
		self.change_home("/home/exaluno/" + self.login) and self.change_shell("/bin/false"))
	self.log("Conta '{0}' desativada. Status: {1}".format(self.login, str(results)))
	if not reduce(lambda a, b: a and b, results.values()):
		return ErrorString("Erro ao desativar conta. Verifique 'DB/usuarios/historicos/{0}' para detalhes.".format(self.nid))
	else:
		return "Conta '{0}' desativada com sucesso.".format(self.login)

def description():
	return "Desativa uma conta, mantendo apenas o e-mail."
