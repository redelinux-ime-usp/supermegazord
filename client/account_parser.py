#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Accounts parser: Trabalha em cima do lib.account
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def search_accounts(atype, u):
	import supermegazord.lib.account as account
	import supermegazord.lib.tools as tools
	if atype == 'all':
		return account.search(u, 'nid') | account.search(u, 'login') | account.search(u, 'name')
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
			curso = (str(curso) + " "*7)[:7]
			ingresso = (str(ingresso) + " "*10)[:10]

			print login + "|" + nid + " |" + curso + "|" + ingresso + "| " + nome
			
	def script_parser(args):
		import supermegazord.lib.account as account
		acc = account.from_login(args.user)
		if not acc:
			print "Erro: usuário '{0}' não encontrado.".format(args.user)
			return
		resp = acc.run_script(args.scriptname)
		if not resp:
			print "Erro ao rodar script '{0}' na conta '{1}':\n>> {2}".format(args.scriptname, args.user, str(resp))
		else:
			print resp

	account_parse.description = "Manipulates the system's accounts."
	subparsers = account_parse.add_subparsers(help="The account manipulation subsystem to run.")

	search = subparsers.add_parser('search', 
		description="Searches for accounts in the system. Lists the accounts' login, nid, group, ingresso and name.")
	search.add_argument('--type', choices=['nid', 'login', 'name', 'all'], dest='type', default='all',
		help="How to parse the query. All means all the others at the same time. Defaults to 'all'.")
	search.add_argument('user', metavar='query', nargs='+',
		help="The search query. Multiple arguments means more results.")
	search.set_defaults(func=search_parser)

	import supermegazord.lib.account as account
	script = subparsers.add_parser('script', description="Executes external scripts on the given account.")
	script.add_argument('scriptname', choices=list(account.list_scripts()), help="The name of the script to run.")
	script.add_argument('user', help="Login used to find the account to execute the script on.")
	script.set_defaults(func=script_parser)
