#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Precadastro parser: Ferramentas para a página web do pré-cadastro.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-01-19

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def prepare_parser(megazordparser):
	import supermegazord.lib.precadastro as precadastrodb

	def verifica_parser(args):
		import supermegazord.lib.account as account
		import supermegazord.lib.jupinfo as jupinfo
		import supermegazord.lib.tools as tools

		if args.nid:
			if not jupinfo.from_nid(args.nid):
				print 'inexistente'
			elif account.from_nid(args.nid):
				print 'usado'
			elif precadastrodb.fetch(args.nid) != None:
				print 'precadastro'
			else:
				print 'livre'
		
		if args.login:
			if account.from_login(args.login):
				print 'usado'
			elif precadastrodb.search('login', args.login) != None:
				print 'precadastro'
			elif not tools.valida_login(args.login):
				print 'invalido'
			else:
				print 'livre'
	
	def adiciona_parser(args):
		if not args.password:
			import getpass
			args.password = getpass.getpass("Password: ")
		if precadastrodb.insert(args.nid, args.login, args.email, args.password):
			print "sucesso"
		else:
			print "erro"
	
	def lista_parser(args):
		import supermegazord.lib.jupinfo as jupinfo
		for p in precadastrodb.list_all():
			print jupinfo.from_nid(p['nid']).__str__() + "; Login: " + p['login']

	def finaliza_parser(args):
		if precadastrodb.finaliza_cadastro(args.nid):
			print "Cadastro do NID '%s' finalizado com sucesso." % args.nid
			print
			print "\033[1;31mDevolva a carteirinha para o usuário!\033[0m"
		else:
			print "Erros no cadastro. Verifique o log para maiores detalhes."
	
	def remove_parser(args):
		precadastrodb.remove(args.nid)

	precadastro_parse = megazordparser.add_parser("precadastro", help="Manipula os pré-cadastros.")
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
	adiciona.add_argument('--email', required=True)
	adiciona.add_argument('--password')

	lista = subparsers.add_parser('lista', help="Lista todos os pré-cadastros.")
	lista.set_defaults(func=lista_parser)

	finaliza = subparsers.add_parser('finaliza')
	finaliza.set_defaults(func=finaliza_parser)
	finaliza.add_argument('nid')

	remove = subparsers.add_parser('remove')
	remove.set_defaults(func=remove_parser)
	remove.add_argument('nid')


