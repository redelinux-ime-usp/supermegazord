#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Watchman: Monitora o estado das máquianas da rede.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-05 por henriquelima

if __name__ != "__main__":
	print "Esse arquivo deve ser rodado apenas como um script."
	quit()

import os
import sys
sys.path.append(os.path.expandvars("$HOME"))

from supermegazord.scripts import watchman
import curses
import signal

class Screen:
	def __init__(self, screen):
		self.screen = screen

	def Width(self):
		height, width = self.screen.getmaxyx()
		return width

	def Clear(self):
		self.screen.clear()

	def Draw(self):
		self.screen.refresh()
	
	def Screen(self):
		return self.screen

quit = False

def signal_int(signalnum, handler):
	global quit
	quit = True

# O wrapper impede que o terminal fique zuado caso de alguma merda no script
def main(stdscr):
	stdscr.nodelay(True)
	screenobj = Screen(stdscr)

	watchman.Init(screenobj)
	watchman.Run()
	
	global quit
	quit = False
	while not quit:
		c = stdscr.getch()
		if c == curses.KEY_RESIZE:
			screenobj.Clear()
			watchman.Resize(screenobj)
		elif c == ord('q'):
			quit = True
		elif c == ord('u'):
			watchman.Update()

if len(sys.argv) == 1:
	signal.signal(signal.SIGINT, signal_int)
	curses.wrapper(main)
	watchman.Close()
else:
	checkfor = 1
	stats = 0
	group = 'all'
	for arg in sys.argv[1:]:
		if arg == "--up" or arg == "-u":
			checkfor = 1
		elif arg == "--down" or arg == "-d":
			checkfor = 0
		elif arg == "--unknown":
			stats = 2
		elif arg == "--who" or arg == "-w":
			stats = 1
		else:
			group = arg
	from supermegazord.db import machines
	from supermegazord.lib import ping
	l = machines.list(group)
	ping.Run(l)
	if stats != 0:
		from supermegazord.lib import busy
		busy.Run(l)
		busy.Wait()
	ping.Wait()
	for m in l:
		if m.Power() == checkfor:
			if stats == 2 and m.StatsAvaiable():
				continue
			print m.hostname,
			if stats == 1:
				for user in m.userlist:
					print user,
			print

