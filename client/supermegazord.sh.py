#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Supermegazord: Executável principal do Super Megazord 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-05029

if __name__ != "__main__":
	print "Esse arquivo deve ser rodado apenas como um script."
	quit()

import sys, argparse
import supermegazord.db.machines as machines

if len(sys.argv) == 1:
	print("Insert curses client here.")
	quit(0)

def machines_parser(args):
	if not isinstance(args.group, list): args.group = [args.group]
	for group in args.group:
		for m in machines.list(group):
			print m.__class__.__dict__[args.print_method](m)

def users_parser(args):
	print "USER!"

parser = argparse.ArgumentParser(description='Super Megazord.')
subparsers = parser.add_subparsers(help='Possíveis scripts')


# Machine
mach_parse = subparsers.add_parser('machines')
print_val = mach_parse.add_mutually_exclusive_group(required=False)
print_val.add_argument('--ip', action='store_const', dest='print_method', const='ip')
print_val.add_argument('--mac', action='store_const', dest='print_method', const='mac')
print_val.set_defaults(print_method='Name')
mach_parse.add_argument('group', choices=machines.groups(), default='all', nargs='*')
mach_parse.set_defaults(func=machines_parser)


user_parse = subparsers.add_parser('users')
user_parse.set_defaults(func=users_parser)

args = parser.parse_args()
args.func(args)

print args

