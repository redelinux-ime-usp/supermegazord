#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Users parser: Wrapper para o db.users para linha de comando. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def prepare_parser(user_parse):
	import supermegazord.db.users as userdata
	def user_parser(args):
		print "    Login    |   NID  |Curso| Ingresso |  Nome" 
		for u in args.user:
			atype = args.type	
			if atype == 'auto':
				if userdata.valida_nid(u):
					atype = 'nid'
				elif userdata.valida_login(u):
					atype = 'login'
				else:
					atype = 'name'
			
			nid = ""
			login = ""
			nome = ""
			jupinfo = None
			if atype == 'nid':
				jupinfo = userdata.get_jupinfo_from_nid(u)
				nid = u
			elif atype == 'login':
				jupinfo = userdata.get_jupinfo_from_login(u)
				login = u

			elif atype == 'name':
				#TODO
				print "Suporte a procurar por nome não implementado"
				continue

			if jupinfo:
				if nid == "": nid = jupinfo.nid
				curso = jupinfo.curso
				ingresso = jupinfo.ingresso
				if nome == "": nome = jupinfo.nome

			# Trata tamanhos
			nid = (" "*8 + str(nid))[-8:]
			curso = (str(curso) + " "*5)[:5]

			print " "*12, "|" + nid + "|" + curso + "|" + ingresso + "|" + nome

	import argparse
	user_parse.add_argument('--type', choices=['nid', 'login', 'name', 'auto'], dest='type', default='auto')
	user_parse.add_argument('user', nargs='+')

	user_parse.set_defaults(func=user_parser)

