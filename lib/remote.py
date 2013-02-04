# -*- coding: utf-8 -*-

# Remote: Permite a manipulação de máquinas remotas.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import subprocess
import supermegazord.db.path as path

import paramiko
import sys

def connect(destination, user = "megazord"):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(destination, username=user, key_filename=path.MEGAZORD_DB + "secrets/keys/" + destination)
		return ssh
	except:
		print "Falha ao conectar em '" + destination + "':", sys.exc_info()[1]
		return None

def run_script(destination, script, user = "megazord"):
	ssh = connect(destination, user)
	if not ssh: return -1
	
	chan = ssh.get_transport().open_session()
	try:
		chan.exec_command(script)
	except:
		return -1
	ret = chan.recv_exit_status()
	print chan.recv_stderr(200),
	return ret

def run_remote_batch(server_list, command, user = "megazord"):
	results = {}
	for server in server_list:
		results[server] = run_script(server, command, user)
	return results

def run_script_with_localpipe(host, script_path, pipe, user = "root"):
	return subprocess.call([pipe + " | ssh -i " + path.MEGAZORD_DB + "secrets/keys/" + host + " -l " + user + " " + host + " " + script_path], shell=True)

def copy_file(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", "-i" + path.MEGAZORD_DB + "secrets/keys/" + host, source_path, user + "@" + host + ":" + target_path], stdout=devnull)

def copy_files(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", "-i" + path.MEGAZORD_DB + "secrets/keys/" + host, "-r", source_path, user + "@" + host + ":" + target_path], stdout=devnull)
