# -*- coding: utf-8 -*-


# Precadastro: Armazena precadastros em um arquivo.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-01-20

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import sqlite3

def _connect():
	import supermegazord.db.path as path
	conn = sqlite3.connect(path.MEGAZORD_DB + "usuarios/precadastro.sqlite3")
	return conn

def setup_table():
	try:
		conn = _connect()
		c = conn.cursor()
		c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='precadastro'")
		if not c.fetchone():
			c.execute('''CREATE TABLE precadastro (nid, login, password, time)''')
			conn.commit()
		conn.close()
	except:
		pass
	
setup_table()

def insert(nid, login, password):
	import time
	conn = _connect()
	c = conn.cursor()
	c.execute("SELECT * from precadastro WHERE nid=?", (nid,))
	if c.fetchone() != None:
		conn.close()
		return False

	c.execute("INSERT into precadastro VALUES (?, ?, ?, ?)",
			  (nid, login, password, time.time()))
	conn.commit()
	conn.close()
	return True

def search(field, value):
	conn = _connect()
	c = conn.cursor()
	c.execute("SELECT * from precadastro WHERE " + field + "=?", (value,))
	data = c.fetchone()
	conn.close()
	if not data: return None
	return {
		'nid': data[0],
		'login': data[1],
		'password': data[2],
		'time': data[3]
	}

def fetch(nid):
	return search('nid', nid)

def remove(nid):
	conn = _connect()
	c = conn.cursor()
	c.execute("DELETE FROM precadastro WHERE nid=?", (nid,))
	conn.commit()
	conn.close()

def list_all():
	conn = _connect()
	c = conn.cursor()
	resp = []
	for i in c.execute("SELECT * from precadastro"):
		resp.append({ 'nid': i[0], 'login': i[1] })
	conn.close()
	return resp
	

PRECADASTRO_MAX_DAYS = 30
def finaliza_cadastro(nid):
	import supermegazord.db.users        as users
	import supermegazord.db.path         as path 
	import supermegazord.lib.jupinfo     as jupinfo
	import supermegazord.lib.precadastro as precadastro
	import supermegazord.lib.group       as megazordgroup
	from   supermegazord.lib.account import Account
	import supermegazord.lib.kerbwrap    as kerbwrap
	import supermegazord.lib.remote      as remote
	import time, datetime

	data = fetch(nid)
	if not data: return False

	if datetime.timedelta(0, time.time() - int(data['time'])).days > PRECADASTRO_MAX_DAYS:
		remove(nid)
		return False

	info  = jupinfo.from_nid(nid)
	if not info: raise Exception("NID dado não possui Jupinfo.")

	uid   = users.get_next_uid()
	group = megazordgroup.from_name(info.curso)
	if not group: raise Exception("Jupinfo possui curso inválido: " + info.curso)
	home  = "/home/" + group.name + "/" + data['login']

	newuser = Account(uid, group.gid, data['login'], info.nome, home, "/bin/bash", nid)

	status = {}
	status['limpeza']  = users.unban_login(newuser.login) # Step 1
	status['passwd']   = newuser.add_to_ldap()
	status['kerberos'] = kerbwrap.add_user(newuser.login, data['password']) == 0

	status['home']     = remote.run_script_with_localpipe("nfs", 
									"sudo /megazord/scripts/cria_conta " + newuser.login + " " + newuser.group.name,
									"tar c -C " + path.MEGAZORD_DB + "usuarios skel/", "megazord") == 0
	
	status['print']    = remote.run_script("printer", "sudo /megazord/scripts/cria_conta " + newuser.login + " " + newuser.group.name, "megazord") == 0
	status['listas']   = remote.run_script("mail",    "sudo /megazord/scripts/cria_conta " + newuser.login + " " + newuser.group.name, "megazord") == 0
	
	msg = "Conta " + newuser.login + (" (%s) aberta\n" % newuser.group.name) + ("NID: %s;" % newuser.nid) + " Nome: %s\n" % newuser.name
	status['historico'] = users.add_history_by_nid(newuser.nid, msg)

	newuser.log("Conta '{0}' ({1}) aberta. Nome: {2}; Status: {3}".format(newuser.login, newuser.group.name, newuser.name, str(status)))
	
	# Remove o precadastro
	remove(nid)

	result = True
	for x in status: result = result and status[x]

	return result
