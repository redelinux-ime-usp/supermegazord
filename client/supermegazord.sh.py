#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Supermegazord: Executável principal do Super Megazord 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-05-29

if __name__ != "__main__":
	print "Esse arquivo deve ser rodado apenas como um script."
	quit()

import sys, argparse

if len(sys.argv) == 1:
	import supermegazord.client.curse.curse_client as cursescli
	cursescli.Run()
	quit(0)

parser = argparse.ArgumentParser(description='Super Megazord.')

subparsers = parser.add_subparsers(help='Possíveis scripts')

import machine_parser
machine_parser.prepare_parser(subparsers.add_parser('machines'))

import users_parser
users_parser.prepare_parser(subparsers.add_parser('users'))

args = parser.parse_args()
args.func(args)
