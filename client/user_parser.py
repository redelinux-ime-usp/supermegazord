#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Users parser: Wrapper para o db.users para linha de comando. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

import supermegazord.db.users as userdata

def validate_type(atype, val):
	if atype == 'auto':
		if userdata.valida_nid(val):
			atype = 'nid'
		elif userdata.valida_login(val):
			atype = 'login'
		else:
			atype = 'name'
	return atype
	
def get_data(atype, u):
	login = nid = curso = ingresso = nome = "n/a"

	jupinfo = None
	if atype == 'nid':
		jupinfo = userdata.get_jupinfo_from_nid(u)
		nid = u
	elif atype == 'login':
		jupinfo = userdata.get_jupinfo_from_login(u)
		login = u
	elif atype == 'name':
		pass

	if jupinfo:
		nid = jupinfo.nid
		curso = jupinfo.curso
		ingresso = jupinfo.ingresso
		nome = jupinfo.nome

	return login, nid, curso, ingresso, nome

def prepare_parser(user_parse):

	def user_parser(args):
		print "   Login    |   NID   | Curso | Ingresso |   Nome" 
		for u in args.user:
			atype = validate_type(args.type, u)
			login, nid, curso, ingresso, nome = get_data(atype, u)

			# Trata tamanhos
			login = (str(login) + " "*12)[:12]
			nid = (" "*8 + str(nid))[-8:]
			curso = (str(curso) + " "*6)[:6]
			ingresso = (str(ingresso) + " "*10)[:10]

			print login + "|" + nid + " | " + curso + "|" + ingresso + "| " + nome

	import argparse
	user_parse.add_argument('--type', choices=['nid', 'login', 'name', 'auto'], dest='type', default='auto')
	user_parse.add_argument('user', nargs='+')

	user_parse.set_defaults(func=user_parser)

