# -*- coding: utf-8 -*-

def main(self):
	import supermegazord.lib.tools as tools
	import supermegazord.lib.kerbwrap as kerbwrap
	password = tools.generate_password()
	error = False
	if not kerbwrap.user_exists(self.login):
		error = (kerbwrap.add_user(self.login, password) != 0)
	else:
		error = (kerbwrap.change_password(self.login, password) != 0)

	if error:
		return "Ocorreu um erro ao mudar a senha e ao adicionar" + (
				" o principal '{0}' no kerberos.".format(self.login))
	else:
		return ("Senha mudada com sucesso.\n" +
				"Nova senha: '" + password + "'\n" +
				"\nDEVOLVA A CARTEIRINHA DO USUÁRIO.")

def description():
	return "Gera uma senha nova para a conta."

