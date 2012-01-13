#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-10
# Modificado em: 2011-08-10 por henriquelima

# Módulo de cores. Define as cores usadas pelo megazord

import curses

BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = None

def init():
	curses.init_pair(1, curses.COLOR_WHITE,  curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
	curses.init_pair(50, curses.COLOR_BLACK, curses.COLOR_BLACK)
	curses.init_pair(51, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(52, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(53, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(54, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(55, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(56, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(57, curses.COLOR_WHITE, curses.COLOR_BLACK)

	global BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
	BLACK   = curses.color_pair(50)
	RED     = curses.color_pair(51)
	GREEN   = curses.color_pair(52)
	YELLOW  = curses.color_pair(53)
	BLUE    = curses.color_pair(54)
	MAGENTA = curses.color_pair(55)
	CYAN    = curses.color_pair(56)
	WHITE   = curses.color_pair(57)
