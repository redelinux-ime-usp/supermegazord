# -*- coding: utf-8 -*-

# Remote: Permite a manipulação de máquinas remotas.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import subprocess
import supermegazord.db.path as path

def run_script(host, script_path, user = "root"):
	return subprocess.call(["ssh", "-i" + path.MEGAZORD_DB + "secrets/keys/" + host, "-l" + user, host, script_path])

def run_script_with_localpipe(host, script_path, pipe, user = "root"):
	return subprocess.call([pipe + " | ssh -i " + path.MEGAZORD_DB + "secrets/keys/" + host + " -l " + user + " " + host + " " + script_path], shell=True)

def copy_file(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", "-i" + path.MEGAZORD_DB + "secrets/keys/" + host, source_path, user + "@" + host + ":" + target_path], stdout=devnull)

def copy_files(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", "-i" + path.MEGAZORD_DB + "secrets/keys/" + host, "-r", source_path, user + "@" + host + ":" + target_path], stdout=devnull)
