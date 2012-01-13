# -*- coding: utf-8 -*-

# DB: Fornece uma interface simples para acesso à bancos de dados.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-17 
# Modificado em: 2012-01-13 por henriquelima

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import path
from ..lib.machine import Machine

machines = dict()
machines['all'] = list()

def open_list(source, group):
	f = open(path.MEGAZORD + "/db/" + source, "r")
	machines[group] = list()
	for raw in f:
		hostname = raw.replace('\n','')
		machine = Machine(hostname, None)
		machines['all'].append(machine)
		machines[group].append(machine)

open_list("lista_122", "122")
open_list("lista_125a", "125a")
open_list("lista_125b", "125b")
open_list("lista_126", "126")
open_list("lista_258", "258")
machines['clients'] = list(machines['all'])
open_list("lista_servidores", "servers")

machines['aquario'] = machines['122']
machines['corredor'] = machines['125a']
machines['admin'] = machines['125b']
machines['herois'] = machines['126']
machines['bcc'] = machines['258']

def list(group):
	return machines[group]

def groups():
	return d.keys()
