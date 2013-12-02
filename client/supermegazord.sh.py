#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Supermegazord: Executável principal do Super Megazord 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-05-29

if __name__ != "__main__":
	print "Esse arquivo deve ser rodado apenas como um script."
	quit()

import sys 
import locale
locale.setlocale(locale.LC_ALL, '')

import supermegazord.lib.tools as tools
tools.log("system", "Executable called with: " + str(sys.argv))

def call_curses_interface(args):
	import supermegazord.client.newcurses.curse_client as cursescli
	cursescli.Run()

# No caso de nenhum argumento de linha de comando, rode a interface curses!
if len(sys.argv) == 1:
	call_curses_interface(None)
	quit(0)

import argparse # Biblioteca do Python

# Criando o argparse principal.
parser = argparse.ArgumentParser(description='Main executable for the Supermegazord.')

# Esse parser principal delega todo o trabalho para diversos outros parsers, definidos em outros módulos
subparsers = parser.add_subparsers(
	help="Possible submodules to execute. Defaults to 'curses'.", metavar="subsystem")

# Carregando os outros módulos, e adicionando seus parsers
import machine_parser, account_parser, watchman_parser, precadastro_parser
machine_parser.prepare_parser(subparsers)
account_parser.prepare_parser(subparsers)
watchman_parser.prepare_parser(subparsers)
precadastro_parser.prepare_parser(subparsers)

# Adicionando o módulo de curses como opção.
subparsers.add_parser('curses', help="An interactive interface.", 
	description="An interactive interface to search and operate on functions " +
	"of the Supermegazord system.").set_defaults(func=call_curses_interface)


# Analisando os argumentos da linha de comando...
# O módulo argparse garante que args é válido, pois termina a execução em caso de erro
args = parser.parse_args()

tools.log("system", "Executable running: " + str(args))

# Delega a execução para o módulo escolhido pelo usuário.
args.func(args)

