#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# DB: Fornece uma interface simples para acesso à bancos de dados.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-17 
# Modificado em: 2012-01-13 por henriquelima

import json
from supermegazord.db import path
from supermegazord.lib.machine import Machine

machines = dict()

def open_list(source):
	result = list()
	try:
		with open(path.MEGAZORD_DB + "/maquinas/" + source + ".conf", "r") as f:
			fulldata = json.load(f)
	except ValueError, e:
		raise Exception("Erro no arquivo '{0}': {1}".format(path.MEGAZORD_DB + "/maquinas/" + source + ".conf", str(e)))

	for hostname, data in fulldata.iteritems():
		mac = data['mac']
		ip = data['ip']
		machine = Machine(hostname, ip, mac, None)
		if 'aliases' in data:
			machine.aliases.extend(data['aliases'])
		result.append(machine)
	return result

with open(path.MEGAZORD_DB + "/maquinas/grupos.conf", "r") as f:
	grupos_conf = json.load(f)

for arq in grupos_conf['arquivos']:
	machines[arq.encode("UTF-8")] = open_list(arq)

for nome, l in grupos_conf['conjuntos'].iteritems():
	nome = nome.encode("UTF-8")
	machines[nome] = list()
	for membro in l:
		machines[nome].extend(machines[membro.encode("UTF-8")])

for apelido, nome in grupos_conf['apelidos'].iteritems():
	machines[apelido.encode("UTF-8")] = machines[nome.encode("UTF-8")]

def list(group):
	return machines[group]

def groups():
	return machines.keys()

def files():
	return grupos_conf['arquivos']

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 1:
		print "%s: grupo" % sys.argv[0]
	else:
		try:
			for m in machines[sys.argv[1]]:
				print m.hostname
		except:
			print "Erro: grupo %s inexistente" % sys.argv[1]
