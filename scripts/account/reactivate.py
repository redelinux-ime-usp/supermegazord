# -*- coding: utf-8 -*-


def main(self):
	if self.group.name != "exaluno": return "Conta não está inativa."
	from supermegazord.lib.tools import ErrorString
	import supermegazord.lib.remote as remote
	import supermegazord.lib.group as megazordgroup
	group = None
	for g in megazordgroup.all():
		if g.name != "olimpo" and g.name != "imortais" and self.login in g.members:
			group = g
	if not group:
		raise Exception("Nenhum grupo válido no qual é membro secundário")
	status = group.remove_member(self) and self.change_group(group) and self.change_home("/home/%s/%s" % (group.name, self.login))
	command = "sudo /megazord/scripts/reativa_conta %s %s" % (self.login, self.group.name)
	results = remote.run_remote_batch(['mail', 'printer', 'nfs'], command, "megazord")
	results['ldap'] = status and self.change_shell("/bin/bash")
	self.log("Conta '{0}' re-ativada. Status: {1}".format(self.login, str(results)))
	if not reduce(lambda a, b: a and b, results.values()):
		return ErrorString("Erro ao re-ativar a conta. Verifique 'DB/usuarios/historicos/{0}' para maiores detalhes.".format(self.nid))
	else:
		return "Conta '{0}' re-ativada com sucesso.".format(self.login)

def description():
	return "Reativa uma conta recentemente desativada."
