#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Machine parser: Wrapper para o db.machines para linha de comando. 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-06-22

if __name__ == "__main__":
	print "Esse arquivo é um módulo."
	quit()

def prepare_parser(user_parse):
	def user_parser(args):
		print "hai"

	import argparse
	user_parse.set_defaults(func=user_parser)

