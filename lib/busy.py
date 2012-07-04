# -*- coding: utf-8 -*-

# Busy: Verifica quais máquinas estão ocupadas 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-05 por henriquelima

import socket
import threads

PORT = 10
BUFSIZ = 1024

num_left = 0

def Busy(machine, command):
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

#wraps system ping command
def checker(machine):
	global num_left
	num_left -= 1
	if machine.Power() == False:
		return
	data = Busy(machine, 'who')
	if data == False:
		machine.SetStatsAvaiability(False)
	elif len(data) > 0:
		users = []
		for userinfo in data.split('\n'):
			u = userinfo.split(' ')[0]
			if u not in users:
				users.append(u)
		machine.SetUserList(users)

def Run(machines):
	if type(machines) != list:
		return checker(machines)
	global num_left
	num_left += len(machines)
	threads.Run(checker, machines)

def Wait():
	threads.Wait()

def Idle():
	return num_left == 0
