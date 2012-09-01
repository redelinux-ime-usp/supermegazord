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
machines['all'] = list()

def open_list(source, group, toall = True):
	machines[group] = list()

	f = open(path.MEGAZORD_DB + "/maquinas/" + source + ".conf", "r")
	fulldata = json.load(f)
	for hostname, data in fulldata.iteritems():
		mac = data['mac']
		ip = data['ip']
		machine = Machine(hostname, ip, mac, None)
		if 'aliases' in data:
			machine.aliases.extend(data['aliases'])
		if toall: machines['all'].append(machine)
		machines[group].append(machine)

open_list("122", "122")
open_list("125a", "125a")
open_list("125b", "125b")
open_list("126", "126")
open_list("258", "258")
machines['clients'] = list(machines['all'])
open_list("servidores", "servers")
open_list("impressoras", "printers", False)

machines['aquario']  = machines['122']
machines['admin']    = machines['125a']
machines['corredor'] = machines['125b']
machines['herois']   = machines['126']
machines['bcc']      = machines['258']

def list(group):
	return machines[group]

def groups():
	return machines.keys()

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
