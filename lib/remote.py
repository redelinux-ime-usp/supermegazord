# -*- coding: utf-8 -*-

# Remote: Permite a manipulação de máquinas remotas.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import subprocess
import supermegazord.db.path as path
import paramiko, socket
import sys

def _log(s):
	import supermegazord.lib.tools as tools
	tools.log("remote", s)

def connect(destination, user = "megazord"):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(destination, username=user, key_filename=path.MEGAZORD_DB + "secrets/keys/" + destination)
		return ssh
	except:
		print "Falha ao conectar em '" + destination + "':", sys.exc_info()[1]
		return None

def run_script(destination, script, user = "megazord", want_return = True):
	ssh = connect(destination, user)
	if not ssh: return -1
	_log("Start running at {0} as {1}: {2}".format(destination, user, script))
	chan = ssh.get_transport().open_session()
	chan.settimeout(60)
	try:
		chan.exec_command(script)
	except paramiko.SSHException:
		return False
	if want_return:
		try:
			err = chan.recv_stderr(200)
			_log("Finished.")
			if len(err) > 0:
				print err
			if chan.exit_status_ready():
				return chan.recv_exit_status() == 0
			return len(err) == 0
		except socket.timeout:
			return False
	_log("Finished.")

def run_remote_batch(server_list, command, user = "megazord", want_return = True):
	results = {}
	for server in server_list:
		results[server] = run_script(server, command, user, want_return)
	return results

def run_script_with_localpipe(host, script_path, pipe, user = "root"):
	return subprocess.call([pipe + " | ssh -i " + path.MEGAZORD_DB + "secrets/keys/" + host + " -l " + user + " " + host + " " + script_path], shell=True)

def copy_file(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", "-i" + path.MEGAZORD_DB + "secrets/keys/" + host, source_path, user + "@" + host + ":" + target_path], stdout=devnull)

def copy_files(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", "-i" + path.MEGAZORD_DB + "secrets/keys/" + host, "-r", source_path, user + "@" + host + ":" + target_path], stdout=devnull)
