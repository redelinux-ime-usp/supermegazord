#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Watchman Parser: Ferramenta command-line que determina quais máquinas da rede estão ligadas/desligadas.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-01-19

def prepare_parser(watch_parse):
	import supermegazord.db.machines as machines 
	def watchman_parser(args):
		import supermegazord.lib.ping as ping
		l = machines.list(args.group)
		ping.Run(l)
		if args.stats != 0:
			import supermegazord.lib.busy as busy
			busy.Run(l)
			busy.Wait()
		ping.Wait()
		for m in l:
			if m.Power() == args.checkfor:
				if args.stats == 2 and m.StatsAvaiable():
					continue
				print m.hostname,
				if args.stats == 1:
					for user in m.user_list:
						print user,
				print

	import argparse
	check_arg = watch_parse.add_mutually_exclusive_group(required=False)
	check_arg.add_argument('--up'  , '-u', action='store_const', dest='checkfor', const=1)
	check_arg.add_argument('--down', '-d', action='store_const', dest='checkfor', const=0)
	check_arg.set_defaults(checkfor=0)
	
	stats_arg = watch_parse.add_mutually_exclusive_group(required=False)
	stats_arg.add_argument('--unknown',    action='store_const', dest='stats', const=2)
	stats_arg.add_argument('--who',  '-w', action='store_const', dest='stats', const=1)
	stats_arg.set_defaults(stats=0)

	watch_parse.add_argument('group', choices=machines.groups(), default='all', nargs='?', metavar='group', 
							help="Machine to group to operate on. Defaults to 'all'.")
	watch_parse.set_defaults(func=watchman_parser)
