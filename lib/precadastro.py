# -*- coding: utf-8 -*-


# Precadastro: Armazena precadastros em um arquivo.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-01-20

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import MySQLdb

def _connect():
	import supermegazord.db.path as path
	conn = MySQLdb.connect("www", "precadastro", "RyWj6vRd8CjFPjUG", "megazord")
	return conn

def insert(nid, login, email, password):
	import supermegazord.lib.tools as tools
	if not tools.valida_nid(nid) or not tools.valida_login(login) or type(password) != str:
		return False
	import supermegazord.lib.jupinfo as jupinfo
	if not jupinfo.from_nid(nid) or len(password) < 6:
		return False
	import supermegazord.lib.crypt as crypt
	crypt_password = crypt.encrypt(password, ":(){:|:&};:")
	conn = _connect()
	c = conn.cursor()
	c.execute("SELECT * from precadastro WHERE nid=%s", (nid,))
	if c.fetchone() != None:
		conn.close()
		return False
	c.execute("INSERT INTO precadastro (nid, login, email, password) VALUES (%s, %s, %s, %s)",
			  (nid, login, email, crypt_password))
	conn.commit()
	conn.close()
	return True

def search(field, value):
	conn = _connect()
	c = conn.cursor()
	c.execute("SELECT * from precadastro WHERE " + field + "=%s", (value,))
	data = c.fetchone()
	conn.close()
	if not data: return None
	return {
		'nid': data[0],
		'login': data[1],
		'email': data[2],
		'password': data[3],
		'time': data[4]
	}

def fetch(nid):
	return search('nid', nid)

def remove(nid):
	conn = _connect()
	c = conn.cursor()
	c.execute("DELETE FROM precadastro WHERE nid=%s", (nid,))
	conn.commit()
	conn.close()

def list_all():
	conn = _connect()
	c = conn.cursor()
	resp = []
	c.execute("SELECT * from precadastro")
	for i in c.fetchall():
		resp.append({ 'nid': i[0], 'login': i[1], 'email': i[2] })
	conn.close()
	return resp
	

PRECADASTRO_MAX_DAYS = 30
def finaliza_cadastro(nid):
	import supermegazord.db.path         as path 
	import supermegazord.lib.jupinfo     as jupinfo
	import supermegazord.lib.precadastro as precadastro
	import supermegazord.lib.group       as megazordgroup
	import supermegazord.lib.account	 as account
	import supermegazord.lib.kerbwrap    as kerbwrap
	import supermegazord.lib.remote      as remote
	import supermegazord.lib.tools		 as tools
	import time, datetime

	data = fetch(nid)
	if not data: return False

	info  = jupinfo.from_nid(nid)
	if not info: raise Exception("NID dado não possui Jupinfo.")

	if account.from_login(data['login']) != None:
		raise Exception("Login dado já existe.")
	
	if account.from_nid(nid) != None:
		raise Exception("NID dado já foi utilizado.")

	uid   = tools.get_next_uid()
	group = megazordgroup.from_name(info.curso)
	if not group: raise Exception("Jupinfo possui curso inválido: " + info.curso)
	home  = "/home/" + group.name + "/" + data['login']

	newuser = account.Account(uid, group.gid, data['login'], info.nome, home, "/bin/bash", nid)

	status = {}
	status['limpeza']  = tools.unban_login(newuser.login) # Step 1
	status['passwd']   = newuser.add_to_ldap()
	status['kerberos'] = kerbwrap.add_user(newuser.login, crypt.decrypt(data['password'], ":(){:|:&};:")) == 0
	status['home']     = remote.run_script_with_localpipe("nfs", 
									"sudo /megazord/scripts/cria_conta " + newuser.login + " " + newuser.group.name,
									"tar c -C " + path.MEGAZORD_DB + "usuarios skel/", "megazord") == 0
	status['email']    = remote.run_script("nfs",     "sudo /megazord/scripts/adiciona_forward " + newuser.login + " " + newuser.group.name + " " + data['email'], "megazord")
	status['print']    = remote.run_script("printer", "sudo /megazord/scripts/cria_conta " + newuser.login + " " + newuser.group.name, "megazord")
	status['listas']   = remote.run_script("mail",    "sudo /megazord/scripts/cria_conta " + newuser.login + " " + newuser.group.name, "megazord")
	
	newuser.log("Conta '{0}' ({1}) aberta. Nome: {2}; NID: {3}; Status: {4}".format(newuser.login, newuser.group.name, newuser.name, newuser.nid, str(status)))
	
	# Remove o precadastro
	remove(nid)

	return reduce(lambda a, b: a and b, status.values())
