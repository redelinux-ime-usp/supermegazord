#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Precadastro parser: Ferramentas para a página web do pré-cadastro.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-01-19

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def prepare_parser(precadastro_parse):
	import supermegazord.lib.precadastro as precadastrodb

	def verifica_parser(args):
		import supermegazord.db.users as userdata

		if args.nid:
			if not userdata.get_jupinfo_from_nid(args.nid):
				print 'inexistente'
			elif userdata.nid_to_login(args.nid) != '':
				print 'usado'
			elif precadastrodb.fetch(args.nid) != None:
				print 'precadastro'
			else:
				print 'livre'
		
		if args.login:
			if userdata.login_to_nid(args.login) != '':
				print 'usado'
			elif precadastrodb.search('login', args.login) != None:
				print 'precadastro'
			elif not userdata.valida_login(args.login):
				print 'invalido'
			else:
				print 'livre'
	
	def adiciona_parser(args):
		precadastrodb.insert(args.nid, args.login, args.password)
		print "sucesso"

	subparsers = precadastro_parse.add_subparsers()

	verifica = subparsers.add_parser('status')
	verifica.set_defaults(func=verifica_parser)
	verifica_options = verifica.add_mutually_exclusive_group(required=True)
	verifica_options.add_argument('--nid')
	verifica_options.add_argument('--login')

	adiciona = subparsers.add_parser('adiciona')
	adiciona.set_defaults(func=adiciona_parser)
	adiciona.add_argument('--nid', required=True)
	adiciona.add_argument('--login', required=True)
	adiciona.add_argument('--password', required=True)


