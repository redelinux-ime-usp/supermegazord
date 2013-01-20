#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Precadastro parser: Ferramentas para a página web do pré-cadastro.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-01-19

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def prepare_parser(precadastro_parse):
	def verifica_parser(args):
		import supermegazord.db.users as userdata

		if args.nid:
			if not userdata.get_jupinfo_from_nid(args.nid):
				print 'inexistente'
			elif userdata.nid_to_login(args.nid) != '':
				print 'usado'
			else:
				print 'livre'
		
		if args.login:
			if userdata.login_to_nid(args.login) != '':
				print 'usado'
			else:
				print 'livre'
	
	def cadastra_parser(args):
		import supermegazord.db.path as path
		import json, time
		with open(path.MEGAZORD_DB + "usuarios/precadastro") as f:
			data = json.load(f)
		data[args.nid] = {
			'login': args.login,
			'password': args.password,
			'time': time.time()
		}
		with open(path.MEGAZORD_DB + "usuarios/precadastro", 'w') as f:
			json.dump(data, f, indent=2, separators=(',', ': '))
		print "sucesso"

	subparsers = precadastro_parse.add_subparsers()

	verifica = subparsers.add_parser('status')
	verifica.set_defaults(func=verifica_parser)
	verifica_options = verifica.add_mutually_exclusive_group()
	verifica_options.add_argument('--nid')
	verifica_options.add_argument('--login')

	cadastra = subparsers.add_parser('cadastra')
	cadastra.set_defaults(func=cadastra_parser)
	cadastra.add_argument('--nid', required=True)
	cadastra.add_argument('--login', required=True)
	cadastra.add_argument('--password', required=True)


