#!/usr/bin/env python

import subprocess
import socket
import daemon

#Determines IP Address
HOSTNAME = '' # Symbolic name meaning all available interfaces 
PORT = 15000
BUFSIZ = 1024

#This function takes Bash commands and returns them
def runMegazord(cmd):
    p = subprocess.Popen("/opt/supermegazord/client/supermegazord.sh.py " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subproccess.PIPE)
    out = p.stdout.read().strip() + p.stderr.read().strip()
    return out  #This is the stdout+stderr from the shell command

ADDR = (HOSTNAME, PORT)

#Function to control option parsing in Python
def controller():
	serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			serversock.bind(ADDR)
			break
		except:
			print "Error: failed to bind to port %s, trying again in 10 seconds." % PORT
			import time
			time.sleep(10)
	serversock.listen(2)
	while True:
		clientsock, addr = serversock.accept()
		data = ""
		try: data = clientsock.recv(BUFSIZ)
		except: 
			print "OH NOES, CRASH"
		import re
		if re.compile('^[a-z\- ]+$').match(data):
			clientsock.send(runMegazord(data))
		else:
			clientsock.send("Invalid command: '" + data + "'")
		clientsock.close()
		
with daemon.DaemonContext():
	controller()
