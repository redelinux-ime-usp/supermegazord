#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# DB: Fornece uma interface simples para acesso à bancos de dados.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-17 
# Modificado em: 2012-01-13 por henriquelima

from supermegazord.db import path
from supermegazord.lib.machine import Machine

machines = dict()
machines['all'] = list()

def open_list(source, group, toall = True):
	f = open(path.MEGAZORD_DB + "/maquinas/" + source, "r")
	machines[group] = list()
	for raw in f:
		data = raw.replace('\n','').split('-')
		hostname = data[0]
		machine = Machine(hostname, None)
		if toall: machines['all'].append(machine)
		machines[group].append(machine)

open_list("lista_122", "122")
open_list("lista_125a", "125a")
open_list("lista_125b", "125b")
open_list("lista_126", "126")
open_list("lista_258", "258")
machines['clients'] = list(machines['all'])
open_list("lista_servidores", "servers")
open_list("lista_impressoras", "printers", False)

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
