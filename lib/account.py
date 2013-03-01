# -*- coding: utf-8 -*-

# Account: Fornece a classe Account, que representa a conta de um usuário da rede 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-12

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()
	
cache = {}
scripts = {}
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
		assert self.login, "Account has invalid login."
		assert self.group and self.uid, "Account '{0}' has invalid group and/or UID.".format(self.login)
		if self.uid not in cache:
			cache[self.uid] = self

	def add_to_ldap(self):
		import ldapwrap
		return ldapwrap.add_user(self)

	def change_group(self, newgroup):
		if not isinstance(newgroup, megazordgroup.Group):
			newgroup = megazordgroup.from_name(newgroup)
		if newgroup == None: return False
		import ldapwrap
		result = ldapwrap.change_user_field(self.login, 'gidNumber', newgroup.gid)
		if result: self.group = newgroup
		return result

	def change_home(self, newhome):
		import ldapwrap
		result = ldapwrap.change_user_field(self.login, 'homeDirectory', newhome)
		if result:
			self.home = newhome
		return result

	def change_shell(self, newshell):
		import ldapwrap
		result = ldapwrap.change_user_field(self.login, 'loginShell', newshell)
		if result:
			self.shell = newshell
		return result

	def change_password(self, password):
		self.log("Ocorreu uma mudança de senha.")
		import kerbwrap
		return kerbwrap.change_password(self.login, password) == 0

	def is_in_group(self, group):
		if group.gid == self.group.gid: return True
		return self.login in group.members

	def mail(self, subject, message, source = "Rede Linux <admin@linux.ime.usp.br>"):
		import smtplib
		from email.mime.text import MIMEText
		msg = MIMEText(message, "plain", "utf-8")
		msg['Subject'] = subject
		msg['From'] = source
		msg['To'] = "{0} <{1}@linux.ime.usp.br>".format(self.name, self.login)
		try:
			s = smtplib.SMTP('mail')
			s.sendmail("admin", [self.login], msg.as_string())
			s.quit()
			return True
		except:
			return False

	def log(self, s):
		import datetime
		import supermegazord.db.path as path
		with open(path.MEGAZORD_DB + "usuarios/historicos/" + str(self.nid), "a") as f:
			f.write(str(datetime.datetime.now()) + ": " + s + "\n")

	def run_script(self, scriptname):
		_search_scripts()
		if scriptname not in scripts:
			raise Exception("Script '{0}' doesn't exist.".format(scriptname))
		script = scripts[scriptname]
		if script.extension == ".py":
			l = {}
			execfile(script.path, {}, l)
			assert ('main' in l) and hasattr(l['main'], '__call__'), (
				"Script '{0}' don't have a callable main.".format(scriptname))
			return l['main'](self)
		else:
			raise Exception("Unsupported script extension: {0}".format(script.extension))
		
	def __repr__(self):
		return 'Account("{0}","{1}","{2}","{3}","{4}","{5}","{6}")'.format(self.uid, self.group.gid, self.login, self.name, self.home, self.shell, self.nid)
		
	def __str__(self):
		return "Account[{2}; uid {0}; {1}]".format(self.uid, self.group, self.login)
		
def from_ldap(ldapdata):
	if not ldapdata: return None
	try:
		uid = ldapdata['uidNumber'][0]
		if uid in cache: return cache[uid]

		gid = ldapdata['gidNumber'][0]
		login = ldapdata['uid'][0]
		home = ldapdata['homeDirectory'][0]
		shell = ldapdata['loginShell'][0]

	except KeyError:
		return None
	
	nid  = ('nid' in ldapdata)   and ldapdata['nid'][0] or None
	name = ('gecos' in ldapdata) and ldapdata['gecos'][0] or ldapdata['cn'][0]
	return Account(uid, gid, login, name, home, shell, nid)

def from_login(login):
	import ldapwrap
	return from_ldap(ldapwrap.find_user_by_login(login))

def from_nid(login):
	import ldapwrap
	return from_ldap(ldapwrap.find_user_by_nid(login))

def search(value, field = 'login'):
	if field == 'login':
		restriction = 'uid=*' + value + ('*' if value != '' else '')
	elif field == 'nid':
		restriction = 'nid=' + value
	elif field == 'name':
		restriction = 'cn=*' + value + ('*' if value != '' else '')
	else:
		raise Exception("Unknown restriction field: '{0}'".format(field))
	resp = set()
	import ldapwrap
	data = ldapwrap.query("ou=People", restriction)
	for d in data:
		x = from_ldap(d[1])
		if x: resp.add(x)
	return resp

def _search_scripts():
	if len(scripts) > 0: return
	import supermegazord, collections, os, os.path
	Script = collections.namedtuple("Script", "path extension")
	d = os.path.dirname(supermegazord.__file__) + "/scripts/account/"
	for f in [ f for f in os.listdir(d) if os.path.isfile(os.path.join(d,f)) ]:
		name, ext = os.path.splitext(f)
		if name in scripts:
			raise Exception("More than one script with name '{0}' detected.".format(name))
		scripts[name] = Script(os.path.join(d,f), ext)

def list_scripts():
	_search_scripts()
	return scripts
