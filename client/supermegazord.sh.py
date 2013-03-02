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

def call_curses_interface(args):
	import supermegazord.client.newcurses.curse_client as cursescli
	cursescli.Run()

if len(sys.argv) == 1:
	call_curses_interface(None)
	quit(0)

import argparse, machine_parser, account_parser, watchman_parser, precadastro_parser

parser = argparse.ArgumentParser(description='Main executable for the Supermegazord.')
subparsers = parser.add_subparsers(help="Possible submodules to execute. Defaults to 'curses'.")

machine_parser.prepare_parser(subparsers.add_parser('machines'))
account_parser.prepare_parser(subparsers.add_parser('accounts'))
watchman_parser.prepare_parser(subparsers.add_parser('watchman'))
precadastro_parser.prepare_parser(subparsers.add_parser('precadastro'))

subparsers.add_parser('curses', description="An interactive interface to search and " + 
	"operate on functions of the Supermegazord system.").set_defaults(func=call_curses_interface)

args = parser.parse_args()
args.func(args)
