#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Users parser: Wrapper para o db.users para linha de comando. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def search_accounts(atype, u):
	import supermegazord.lib.account as account
	import supermegazord.lib.tools as tools
	if atype == 'auto':
		if tools.valida_nid(u):
			atype = 'nid'
		else:
			atype = 'login'
	return account.search(u, atype)

def get_data(acc):
	import supermegazord.lib.jupinfo as libjupinfo
	
	login = acc.login
	nid = curso = ingresso = nome = "n/a"

	jupinfo = None
	if acc.nid:
		jupinfo = libjupinfo.from_nid(acc.nid)
	if not jupinfo:
		jupinfo = libjupinfo.from_login(acc.login)

	if jupinfo:
		nid = jupinfo.nid
		curso = jupinfo.curso
		ingresso = jupinfo.ingresso
		nome = jupinfo.nome
	else:
		if acc.nid: nid = acc.nid
		curso = acc.group.name
		nome = acc.name

	return login, nid, curso, ingresso, nome

def prepare_parser(account_parse):

	def search_parser(args):
		print "   Login            |   NID   | Curso | Ingresso |   Nome"
		results = set()
		for u in args.user:
			results |= search_accounts(args.type, u)

		for u in results:
			login, nid, curso, ingresso, nome = get_data(u)

			# Trata tamanhos
			login = (str(login) + " "*20)[:20]
			nid = (" "*8 + str(nid))[-8:]
			curso = (str(curso) + " "*6)[:6]
			ingresso = (str(ingresso) + " "*10)[:10]

			print login + "|" + nid + " | " + curso + "|" + ingresso + "| " + nome
			
	def remove_parser(args):
		import supermegazord.lib.account as account
		acc = account.from_login(args.user)
		if not acc:
			print "Erro: usuário '{0}' não encontrado.".format(args.user)
			return
		if acc.remove():
			print "Conta '{0}' removida com successo.".format(acc.login)
		else:
			print "Erro ao removida conta '{0}'.".format(acc.login)

	def reactivate_parser(args):
		import supermegazord.lib.account as account
		acc = account.from_login(args.user)
		if not acc:
			print "Erro: usuário '{0}' não encontrado.".format(args.user)
			return
		if acc.reactivate():
			print "Conta '{0}' re-ativada com successo.".format(acc.login)
		else:
			print "Erro ao re-ativar conta '{0}'.".format(acc.login)
	
	def deactivate_parser(args):
		import supermegazord.lib.account as account
		acc = account.from_login(args.user)
		if not acc:
			print "Erro: usuário '{0}' não encontrado.".format(args.user)
			return
		if acc.deactivate():
			print "Conta '{0}' desativada com successo.".format(acc.login)
		else:
			print "Erro ao desativar conta '{0}'.".format(acc.login)

	def newpassword_parser(args):
		import supermegazord.lib.account as account
		import supermegazord.db.users as users
		acc = account.from_login(args.user)
		if not acc:
			print "Erro: usuário '{0}' não encontrado.".format(args.user)
			return
		password = users.generate_password()
		if acc.change_password(password):
			print "Nova senha para '{0}': {1}".format(acc.login, password)
		else:
			print "Erro ao renovar senha da conta '{0}'.".format(acc.login)

	subparsers = account_parse.add_subparsers()

	search = subparsers.add_parser('search')
	search.add_argument('--type', choices=['nid', 'login', 'name', 'auto'], dest='type', default='auto')
	search.add_argument('user', nargs='+')
	search.set_defaults(func=search_parser)
	
	remove = subparsers.add_parser('remove')
	remove.add_argument('user')
	remove.set_defaults(func=remove_parser)

	reactivate = subparsers.add_parser('reactivate')
	reactivate.add_argument('user')
	reactivate.set_defaults(func=reactivate_parser)
	
	deactivate = subparsers.add_parser('deactivate')
	deactivate.add_argument('user')
	deactivate.set_defaults(func=deactivate_parser)

	newpassword = subparsers.add_parser('newpassword')
	newpassword.add_argument('user')
	newpassword.set_defaults(func=newpassword_parser)

