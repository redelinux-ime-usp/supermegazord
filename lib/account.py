# -*- coding: utf-8 -*-

# Account: Fornece a classe Account, que representa a conta de um usuário da rede 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-12

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()
	
import supermegazord.lib.group as megazordgroup

class Account:
	def __init__(self, uid, gid, login, name, home, shell, nid = None):
		self.uid = uid
		self.group = megazordgroup.from_gid(gid)
		self.login = login
		self.name = name
		self.home = home
		self.shell = shell
		self.nid = nid

	def change_group(self, newgroup):
		if not isinstance(newgroup, megazordgroup.Group):
			if isinstance(newgroup, int):
				newgroup = megazordgroup.from_gid(newgroup)
			else:
				newgroup = megazordgroup.from_name(newgroup)
		
		if newgroup == None: return False
		import ldapwrap
		result = ldapwrap.change_group(self.login, newgroup.gid)
		if result: self.group = newgroup
		return result

	def add_to_ldap(self):
		import ldapwrap
		return ldapwrap.add_user(self)

	def change_home(self, newhome):
		import ldapwrap
		result = ldapwrap.change_user_field(self.login, 'homeDirectory', newhome)
		if result:
			self.home = newhome
		return result

	def change_password(self, password):
		import kerbwrap
		return kerbwrap.change_password(self.name, password)

	def is_in_group(self, group):
		if group.gid == self.group.gid: return True
		return self.login in group.members

	def activate(self):
		if self.group.name != "exaluno": return True
		import remote
		import supermegazord.db.path as path
		group = None
		for g in megazordgroup.all():
			if g.name != "olimpo" and g.name != "imortais" and self.login in g.members:
				group = g
		if not group:
			raise Exception("Nenhum grupo válido no qual é membro secundário")
		status = group.remove_member(self) and self.change_group(group) and self.change_home("/home/" + group.name + "/" + self.login)
		command = "sudo /megazord/scripts/ativa_conta " + self.login + " " + self.group.name
		results = remote.run_remote_batch(['mail', 'printer', 'nfs'], command, "megazord")
		for s in results: results[s] = (results[s] == 0)
		results['ldap'] = status
		for s in results: status = status and results[s]
		self.log("Conta '{0}' re-ativada. Status: {1}".format(self.login, str(results)))
		return status

	def deactivate(self):
		if self.group.name == "exaluno": return True
		import remote
		import supermegazord.db.path as path
		command = "sudo /megazord/scripts/desativa_conta " + self.login + " " + self.group.name
		results = remote.run_remote_batch(['mail', 'printer', 'nfs'], command, "megazord")
		for s in results: results[s] = (results[s] == 0)
		results['ldap'] = self.group.add_member(self) and self.change_group('exaluno') and self.change_home("/home/exaluno/" + self.login)
		status = True
		for s in results: status = status and results[s]
		self.log("Conta '{0}' desativada. Status: {1}".format(self.login, str(results)))
		return status

	def log(self, s):
		import datetime
		import supermegazord.db.path as path
		with open(path.MEGAZORD_DB + "usuarios/historicos/" + str(self.nid), "a") as f:
			f.write(str(datetime.datetime.now()) + ": " + s + "\n")
		
	def __repr__(self):
		return 'Account({0},{1},"{2}","{3}","{4}","{5}",{6})'.format(self.uid, self.group.gid, self.login, self.name, self.home, self.shell, self.nid)
		
	def __str__(self):
		return "Account[{2}; uid {0}; {1}]".format(self.uid, self.group, self.login)
		
def from_ldap(ldapdata):
	if not ldapdata: return None
	uid = ldapdata['uidNumber'][0]
	gid = ldapdata['gidNumber'][0]
	if 'nid' in ldapdata:
		nid = ldapdata['nid'][0]
	else:
		nid = -1
	login = ldapdata['uid'][0]
	if 'gecos' in ldapdata:
		name = ldapdata['gecos'][0]
	else:
		name = ldapdata['cn'][0]
	home = ldapdata['homeDirectory'][0]
	shell = ldapdata['loginShell'][0]
	return Account(uid, gid, login, name, home, shell, nid)

def from_login(login):
	import ldapwrap
	return from_ldap(ldapwrap.find_user_by_login(login))
