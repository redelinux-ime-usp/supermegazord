# -*- coding: utf-8 -*-

# Remote: Permite a manipulação de máquinas remotas.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import subprocess

def run_script(host, script_path, user = "root"):
	return subprocess.call(["ssh", "-l" + user, host, script_path])

def copy_file(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", source_path, user + "@" + host + ":" + target_path], stdout=devnull)

def copy_files(host, source_path, target_path = "", user = "root"):
	devnull = open('/dev/null')
	return subprocess.call(["scp", "-r", source_path, user + "@" + host + ":" + target_path], stdout=devnull)
