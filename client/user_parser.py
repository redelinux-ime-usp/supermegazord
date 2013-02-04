#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Users parser: Wrapper para o db.users para linha de comando. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

import supermegazord.db.users as userdata

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
	elif atype == 'auto':
		if userdata.valida_nid(u):
			jupinfo = userdata.get_jupinfo_from_nid(u)
			nid = u
		else:
			jupinfo = userdata.get_jupinfo_from_login(u)
			login = u
	
	if jupinfo:
		nid = jupinfo.nid
		curso = jupinfo.curso
		ingresso = jupinfo.ingresso
		nome = jupinfo.nome

	return login, nid, curso, ingresso, nome

def prepare_parser(user_parse):

	def search_parser(args):
		print "   Login            |   NID   | Curso | Ingresso |   Nome" 
		for u in args.user:
			login, nid, curso, ingresso, nome = get_data(args.type, u)

			# Trata tamanhos
			login = (str(login) + " "*20)[:20]
			nid = (" "*8 + str(nid))[-8:]
			curso = (str(curso) + " "*6)[:6]
			ingresso = (str(ingresso) + " "*10)[:10]

			print login + "|" + nid + " | " + curso + "|" + ingresso + "| " + nome

	def reactivate_parser(args):
		import supermegazord.lib.account as account
		acc = account.from_login(args.user)
		if not acc:
			print "Erro: usuário '{0}' não encontrado.\n".format(args.user)
			return
		if acc.reactivate():
			print "Conta '{0}' re-ativada com successo.\n".format(acc.login)
		else:
			print "Erro ao re-ativar conta '{0}'.\n".format(acc.login)
	
	def deactivate_parser(args):
		import supermegazord.lib.account as account
		acc = account.from_login(args.user)
		if not acc:
			print "Erro: usuário '{0}' não encontrado.\n".format(args.user)
			return
		if acc.deactivate():
			print "Conta '{0}' desativada com successo.\n".format(acc.login)
		else:
			print "Erro ao desativar conta '{0}'.\n".format(acc.login)

	subparsers = user_parse.add_subparsers()

	search = subparsers.add_parser('search')
	search.add_argument('--type', choices=['nid', 'login', 'name', 'auto'], dest='type', default='auto')
	search.add_argument('user', nargs='+')
	search.set_defaults(func=search_parser)

	reactivate = subparsers.add_parser('reactivate')
	reactivate.add_argument('user')
	reactivate.set_defaults(func=reactivate_parser)
	
	deactivate = subparsers.add_parser('deactivate')
	deactivate.add_argument('user')
	deactivate.set_defaults(func=deactivate_parser)

