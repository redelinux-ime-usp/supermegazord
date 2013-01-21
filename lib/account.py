# -*- coding: utf-8 -*-

# Account: Fornece a classe Account, que representa a conta de um usuário da rede 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-12

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()
	
import supermegazord.lib.group as megazordgroup

class Account:
	def __init__(self, uid, gid, login, name, home, shell, nid = -1):
		self.uid = uid
		self.group = megazordgroup.from_gid(gid)
		self.login = login
		self.name = name
		self.home = home
		self.shell = shell
		self.password = ''
		self.nid = nid

	def set_nid(self, nid):
		self.nid = nid
		
	def set_password(self, password):
		self.password = password
		
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
		return ldapwrap.add_user_account(self)

	def add_to_kerberos(self):
		import kerbwrap
		return kerbwrap.add_user(self.name, self.password)

	def send_password_update(self):
		import kerbwrap
		return kerbwrap.change_password(self.name, self.password)

	def is_in_group(self, group):
		if group.gid == self.group.gid: return True
		return self.login in group.members

	def activate(self):
		raise Exception("Not yet implemented.")

	def deactivate(self):
		raise Exception("Not yet implemented.")
		
	def __repr__(self):
		return 'Account({0},{1},"{2}","{3}","{4}","{5}",{6})'.format(self.uid, self.group.gid, self.login, self.name, self.home, self.shell, self.nid)
		
	def __str__(self):
		return "Account[{2}; uid {0}; {1}]".format(self.uid, self.group, self.login)
		
def _load_precadastro()
	import supermegazord.db.path as path
	with open(path.MEGAZORD_DB + "usuarios/precadastro") as f:
		return json.load(f)

def _save_precadastro(data)
	import supermegazord.db.path as path
	with open(path.MEGAZORD_DB + "usuarios/precadastro", 'w') as f:
		json.dump(data, f)

def create(nid):
	from supermegazord.db.users import get_next_uid
	import supermegazord.lib.jupinfo as jupinfo
	import json, time, datetime
	precadastro = _load_precadastro()
	if str(nid) not in precadastro:
		return None
	data = precadastro[str(nid)]
	if datetime.timedelta(0, time.time() - int(data['time'])).days > PRECADASTRO_MAX_DAYS:
		del precadastro[str(nid)]


	
	info  = jupinfo.from_nid(nid)
	if not info: raise Exception("NID dado não possui Jupinfo.")

	uid   = get_next_uid()
	login = data['login']
	group = megazordgroup.from_name(info.curso)
	if not group: raise Exception("Jupinfo possui curso inválido: " + info.curso)

	home = "/home/" + group.name + "/" + data['login']

	return True

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
