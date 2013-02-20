#!/usr/bin/env python

import subprocess
import socket
import daemon

#Determines IP Address
HOSTNAME = '' # Symbolic name meaning all available interfaces 
PORT = 15000
BUFSIZ = 1024

valid_commands = [ 'machines', 'watchman', 'precadastro' ]

#This function takes Bash commands and returns them
def runMegazord(cmd):
	sp = cmd.split(' ')
	if sp[0] not in valid_commands:
		return "Permission denied."
	p = subprocess.Popen("/opt/supermegazord/client/supermegazord.sh.py " + cmd.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out = p.stdout.read().strip() + p.stderr.read().strip()
	return out  #This is the stdout+stderr from the shell command

ADDR = (HOSTNAME, PORT)

#Function to control option parsing in Python
def controller():
	serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	fail = False
	while True:
		try:
			serversock.bind(ADDR)
			break
		except:
			fail = True
			print "Error: failed to bind to port %s, trying again in 10 seconds." % PORT
			import time
			time.sleep(10)
	if fail: print "Success."
	serversock.listen(2)
	while True:
		clientsock, addr = serversock.accept()
		data = ""
		try: data = clientsock.recv(BUFSIZ)
		except: 
			print "OH NOES, CRASH"
		import re
		if re.compile('^[a-zA-Z0-9\- \'\.@\+]+$').match(data):
			clientsock.send(runMegazord(data))
		else:
			clientsock.send("Input has illegal chars. Command: '" + data + "'")
		clientsock.close()
	
import sys
if len(sys.argv) > 1 and sys.argv[1] == "-d":
	controller()
else:
	with daemon.DaemonContext():
		controller()
