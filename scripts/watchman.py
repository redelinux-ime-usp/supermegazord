#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Watchman: Monitora o estado das máquianas da rede.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-05 por henriquelima

import curses, time, sys, signal
from threading import Thread
from supermegazord.lib import ping, busy
from supermegazord.lib.machine import Machine
from supermegazord.base import colors

status_colors = []
groups = []
subtitle = None
num_unk = 0
num_up = 0
num_down = 0
num_busy = 0

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

class Group:
	def __init__(self, name, offset, parent):
		self.name = name
		self.height = 0
		self.offset = offset
		self.parent = parent
		self.members = []

	def ColumnSize(self):
		return 13

	def NumColumns(self):
		return max(min(len(self.members),(self.parent.Width()-1) / self.ColumnSize()), 1)

	def Height(self):
		return self.height + 1

	def Width(self):
		return self.ColumnSize() * self.NumColumns()

	def Add(self, machine):
		self.members.append(machine)
		self.height = len(self.members) / self.NumColumns() + 1

	def Reposition(self):
		self.height = len(self.members) / self.NumColumns()
		if len(self.members) % self.NumColumns() != 0:
			self.height += 1
		
	def Offset(self):
		return self.offset + 1

	def Draw(self):
		screen = self.parent.Screen()
		width = self.NumColumns() * self.ColumnSize()
		for x in range(1, width):
			try: screen.addstr(self.offset, x, '═')
			except curses.error: pass

			try: screen.addstr(self.offset + self.height + 1, x, '═')
			except curses.error: pass

			for y in range(1, self.height + 1):
				for x in [0, self.NumColumns()]:
					try: screen.addstr(self.offset + y, x * self.ColumnSize(), '║')
					except curses.error: pass
		
		try: screen.addstr(self.offset, 0, '╔')
		except curses.error: pass

		try: screen.addstr(self.offset + self.height + 1, 0, '╚')
		except curses.error: pass

		try: screen.addstr(self.offset, width, '╗')
		except curses.error: pass

		try: screen.addstr(self.offset + self.height + 1, width, '╝')
		except curses.error: pass

		try: screen.addstr(self.offset, 4, self.name)
		except curses.error: pass
			
		index = 0
		for member in self.members:
			try:
				y = index / self.NumColumns() + 1 # A linha onde esse membro está
				x = 1 + self.ColumnSize() * (index % self.NumColumns()) # 1 da borda esquerda

				screen.addnstr(y + self.offset, x + 1, member.Name(), self.ColumnSize()-1, member.Color())
													# 1 caraceter é reservado para a possível '?'
				if member.StatsAvaiable() == False:
					screen.addstr(y + self.offset, x, '?', colors.MAGENTA)
				index += 1
			except curses.error:
				pass

	def Screen(self):
		return self.parent.Screen()

	def Colors(self, num):
		return status_colors[num]

class Subtitle:
	def __init__(self, offset, parent):
		self.height = 0
		self.offset = offset
		self.parent = parent

	def Draw(self):
		screen = self.parent.Screen()
		try:
			screen.move(self.offset, 0)
			screen.addstr("UNK:", colors.WHITE)
			screen.addstr(("  " + str(num_unk) + ";")[len(str(num_unk)):], colors.WHITE)
			screen.addstr(" UP: ", colors.GREEN)
			screen.addstr(("  " + str(num_up) + ";")[len(str(num_up)):], colors.GREEN)
			screen.addstr(" DOWN:", colors.RED)
			screen.addstr(("  " + str(num_down) + ";")[len(str(num_down)):], colors.RED)
			screen.addstr(" BUSY:", colors.YELLOW)
			screen.addstr(("  " + str(num_busy) + ";")[len(str(num_busy)):], colors.YELLOW)
		except curses.error:
			pass

def DrawGroups():
	while True:
		global num_unk, num_up, num_down, num_busy
		num_unk, num_up, num_down, num_busy = 0, 0, 0,0
		for group in groups:
			group.Draw()
			for machine in group.members:
				if machine.Power() == True:
					num_up += 1
				elif machine.Power() == False:
					num_down += 1
				elif machine.QueryFinished() == False:
					num_unk += 1
				if machine.UserList() != []:
					num_busy += 1
					
		subtitle.Draw()
		time.sleep(0.5)


def Reposition():
	global groups
	offset = 0
	for group in groups:
		group.Reposition()
		group.offset = offset
		offset += group.Height() + 1
	subtitle.offset = offset

def Resize(screenobj):
	Reposition()
	global groups
	for group in groups:
		group.Draw()
	subtitle.Draw()
	screenobj.Draw()

def AddList(l, name, screen):
	global groups
	group = Group(name, 0, screen)
	for machine in l:
		group.Add(machine)
		machine.parent = group
	groups.append(group)

def Init(screen):
	from supermegazord.db import machines
	AddList(machines.list('servers'), "Servidores", screen)
	AddList(machines.list('122'), "122", screen)
	AddList(machines.list('125a'), "125a", screen)
	AddList(machines.list('125b'), "125b", screen)
	AddList(machines.list('126'), "126", screen)
	AddList(machines.list('258'), "258", screen)
	AddList(machines.list('printers'), "Impressoras", screen)
	global subtitle
	subtitle = Subtitle(0, screen)
	Reposition()

def CursesRun():
	global groups
	curses.curs_set(0)
	colors.init()
	global status_colors
	status_colors.insert(0, colors.WHITE)
	status_colors.insert(1, colors.GREEN)
	status_colors.insert(2, curses.color_pair(4))
	status_colors.insert(3, colors.YELLOW)
	Update()
	worker = Thread(target=DrawGroups)
	worker.setDaemon(True)
	worker.start()

def Update():
	if num_unk > 0: return
	machines = []
	for group in groups:
		machines.extend(group.members)
	for machine in machines:
		machine.ResetStatus()
	ping.Run(machines)
	busy.Run(machines)

def Close():
	#Wait until worker threads are done to exit
	ping.Wait()
	busy.Wait()


userquit = False
def signal_int(signalnum, handler):
	global userquit
	userquit = True

# O wrapper impede que o terminal fique zuado caso de alguma merda no script
def main(stdscr):
	stdscr.nodelay(True)
	screenobj = Screen(stdscr)

	Init(screenobj)
	CursesRun()
	
	global userquit
	userquit = False
	while not userquit:
		c = stdscr.getch()
		if c == curses.KEY_RESIZE:
			screenobj.Clear()
			Resize(screenobj)
		elif c == ord('q'):
			userquit = True
		elif c == ord('u'):
			Update()

def Run():
	signal.signal(signal.SIGINT, signal_int)
	curses.wrapper(main)
	Close()

def prepare_parser(watch_parse):
	import supermegazord.db.machines as machines
	def watchman_parser(args):
		print args
		pass

	import argparse
	check_arg = watch_parse.add_mutually_exclusive_group(required=False)
	check_arg.add_argument('--up'  , '-u', action='store_const', dest='checkfor', const=1)
	check_arg.add_argument('--down', '-d', action='store_const', dest='checkfor', const=0)
	check_arg.set_defaults(checkfor=0)
	
	stats_arg = watch_parse.add_mutually_exclusive_group(required=False)
	stats_arg.add_argument('--unknown',    action='store_const', dest='stats', const=2)
	stats_arg.add_argument('--who',  '-w', action='store_const', dest='stats', const=1)
	stats_arg.set_defaults(stats=0)

	watch_parse.add_argument('group', choices=machines.groups(), default='all')
	watch_parse.set_defaults(func=watchman_parser)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		Run()
		sys.exit()

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


