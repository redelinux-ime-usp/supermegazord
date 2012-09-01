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
		for u in args.user:
			atype = args.type	
			if atype == 'auto':
				if userdata.valida_nid(u):
					atype = 'nid'
				elif userdata.valida_login(u):
					atype = 'login'
				else:
					atype = 'name'

			jupinfo = None
			if atype == 'nid':
				jupinfo = userdata.get_jupinfo_from_nid(u)
			elif atype == 'login':
				jupinfo = userdata.get_jupinfo_from_login(u)
			elif atype == 'name':
				#TODO
				print "Suporte a procurar por nome não implementado"
			
			if jupinfo:
				print jupinfo
			else:
				print "'" + u + "' não encontrado."

	import argparse
	user_parse.add_argument('--type', choices=['nid', 'login', 'name', 'auto'], dest='type', default='auto')
	user_parse.add_argument('user', nargs='+')

	user_parse.set_defaults(func=user_parser)

