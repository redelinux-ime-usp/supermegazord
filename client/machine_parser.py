#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Machine parser: Wrapper para o db.machines para linha de comando. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def prepare_parser(megazordparser):
	import supermegazord.db.machines as machines
	def machines_parser(args):
		if not isinstance(args.group, list):
			args.group = [args.group]

		if args.machine_name is not None:
			all_groups = machines.groups()
			machine_groups = []
			for group in all_groups:
				if args.machine_name in (machine.hostname for machine
				                         in machines.list(group)):
					machine_groups.append(group)

			print ','.join(machine_groups)
		else:
			for group in args.group:
				for m in machines.list(group):
					if 'dead' not in m.flags or not m.flags['dead']:
						if args.print_value == "all":
							print m.hostname + "?" + m.ip + "?" + m.mac
						else:
							print m.__dict__[args.print_value]

	mach_parse = megazordparser.add_parser('machines', help="Lists the system's machines.")
	mach_parse.description = "Lists machines as defined by the 'DB/maquinas/grupos.conf' file."
	print_val = mach_parse.add_mutually_exclusive_group(required=False)
	print_val.add_argument('--ip', action='store_const', dest='print_value', const='ip', help="List IPs instead of the hostnames")
	print_val.add_argument('--mac', action='store_const', dest='print_value', const='mac', help="List MAC Addresses instead of the hostnames")
	print_val.add_argument('--all', action='store_const', dest='print_value', const='all', 
	                       help="List hostname, ip and mac address, separated by a '?'")
	print_val.add_argument('--machine-groups', action='store', dest='machine_name', 
	                       help="List groups a machine belongs to, comma-separated")
	print_val.set_defaults(print_value='hostname',machine_name=None)
	mach_parse.add_argument('group', choices=machines.groups(), default='all', nargs='*', metavar='group',
	                        help="Groups to list the machines off. Defaults to 'all'.")
	mach_parse.set_defaults(func=machines_parser)

