#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Machine parser: Wrapper para o db.machines para linha de comando. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def prepare_parser(mach_parse):
	import supermegazord.db.machines as machines
	def machines_parser(args):
		if not isinstance(args.group, list): args.group = [args.group]
		for group in args.group:
			for m in machines.list(group):
				if args.print_value == "all":
					print m.hostname + "?" + m.ip + "?" + m.mac
				else:
					print m.__dict__[args.print_value]

	import argparse
	print_val = mach_parse.add_mutually_exclusive_group(required=False)
	print_val.add_argument('--ip', action='store_const', dest='print_value', const='ip')
	print_val.add_argument('--mac', action='store_const', dest='print_value', const='mac')
	print_val.add_argument('--all', action='store_const', dest='print_value', const='all')
	print_val.set_defaults(print_value='hostname')
	mach_parse.add_argument('group', choices=machines.groups(), default='all', nargs='*')
	mach_parse.set_defaults(func=machines_parser)

