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
	conn = _connect()
	c = conn.cursor()
	c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='precadastro'")
	if not c.fetchone():
		c.execute('''CREATE TABLE precadastro (nid, login, password, time)''')
		conn.commit()
	conn.close()
	
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
