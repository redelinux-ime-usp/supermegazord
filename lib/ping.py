# -*- coding: utf-8 -*-

# Ping: Verifica se uma máquina, ou uma lista de, está acessível. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-05 por henriquelima

import subprocess
import threads

num_left = 0

def Ping(machine):
	return subprocess.call("ping -c 1 -W 2 %s" % machine.hostname,
					 shell=True,
					 stdout=open('/dev/null', 'w'),
					 stderr=subprocess.STDOUT)

#wraps system ping command
def pinger(machine):
	global num_left
	num_left -= 1
	machine.SetPower(not Ping(machine))
	machine.FinishQuery()

def Run(machines):
	if type(machines) != list:
		return Ping(machines)
	global num_left
	num_left += len(machines)
	threads.Run(pinger, machines)

def Wait():
	threads.Wait()

def Idle():
	return num_left == 0
