# -*- coding: utf-8 -*-

# Stats: acessa o rlstats de uma máquina remota
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-03-06

import socket

PORT = 10
BUFSIZ = 1024

def query(machine, command):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ADDR = (machine.hostname, PORT)
	try:
		sock.connect(ADDR)
	except socket.error:
		return False
	sock.send(command)
	data = sock.recv(BUFSIZ)
	sock.close()
	return data
