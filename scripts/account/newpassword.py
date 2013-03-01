# -*- coding: utf-8 -*-

def main(self):
	import supermegazord.lib.tools as tools
	password = tools.generate_password()
	if not self.change_password(password):
		# Adicionar no kerberos
		import supermegazord.lib.kerbwrap as kerbwrap
		if kerbwrap.add_user(self.login, password) != 0:
			return "Ocorreu um erro ao mudar a senha e ao adicionar" + (
					" o principal '{0}' no kerberos.".format(self.login))
	return ("Senha mudada com sucesso.\n" +
			"Nova senha: '" + password + "'\n" +
			"\nDEVOLVA A CARTEIRINHA DO USUÁRIO.")

