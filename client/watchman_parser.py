#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Watchman Parser: Ferramenta command-line que determina quais máquinas da rede estão ligadas/desligadas.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-01-19

def prepare_parser(megazordparser):
	watch_parse = megazordparser.add_parser("watchman",	
					help="Check the status of the system's machines.")
	setup_parser(watch_parse)

def setup_parser(watch_parse):
	import supermegazord.db.machines as machines 
	def watchman_parser(args):
		import supermegazord.lib.machine as libmachine
		import supermegazord.lib.worker as libworker
		
		worker = libworker.Processor()

		statuses = []
		for m in machines.list(args.group):
			statuses.append(libmachine.Status(m))
		
		for status in statuses:
			worker.add_job((status.query_network,))
			if args.stats != 0:
				worker.add_job((status.query_usage,))

		worker.start()
		worker.join()

		for status in statuses:
			if 'dead' in status.machine.flags and status.machine.flags['dead']:
				# Não acuse maquinas marcadas como 'dead' como down.
				continue
			if status.down == args.check_network:
				if args.stats == 2 and status.usage_avaible:
					continue
				print status.machine.hostname,
				if args.stats == 1:
					for user in status.users:
						print user,
				print

	watch_parse.description = "List the system's machines according to their " + (
		"reachable status and more.")
	check_arg = watch_parse.add_mutually_exclusive_group(required=False)
	check_arg.add_argument('--up'  , '-u', action='store_const', dest='check_network', 
		const=False, help="Report reachable machines.")
	check_arg.add_argument('--down', '-d', action='store_const', dest='check_network',
		const=True, help="Report unreachable machines. This is the default operation.")
	check_arg.set_defaults(check_network=True)
	
	stats_arg = watch_parse.add_mutually_exclusive_group(required=False)
	stats_arg.add_argument('--unknown',    action='store_const', dest='stats',
		const=2, help="Skip machines with unknown status.")
	stats_arg.add_argument('--who',  '-w', action='store_const', dest='stats',
		const=1, help="List logged in users along with the machine name.")
	stats_arg.set_defaults(stats=0)

	watch_parse.add_argument('group', choices=machines.groups(), default='all',
		nargs='?', metavar='group', help="Machine to group to operate on. Defaults to 'all'.")
	watch_parse.set_defaults(func=watchman_parser)
