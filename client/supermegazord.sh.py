#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Supermegazord: Executável principal do Super Megazord 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-05-29

if __name__ != "__main__":
	print "Esse arquivo deve ser rodado apenas como um script."
	quit()

import sys 

if len(sys.argv) == 1:
	import supermegazord.client.curse.curse_client as cursescli
	cursescli.Run()
	quit(0)

import argparse, machine_parser, account_parser, watchman_parser, precadastro_parser

parser = argparse.ArgumentParser(description='Super Megazord.')
subparsers = parser.add_subparsers(help='Possíveis scripts')

machine_parser.prepare_parser(subparsers.add_parser('machines'))
account_parser.prepare_parser(subparsers.add_parser('accounts'))
watchman_parser.prepare_parser(subparsers.add_parser('watchman'))
precadastro_parser.prepare_parser(subparsers.add_parser('precadastro'))

args = parser.parse_args()
args.func(args)
