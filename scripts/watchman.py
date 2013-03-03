#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Watchman: Monitora o estado das máquianas da rede.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-05 por henriquelima

import curses, time, sys, signal, collections
from threading import Thread
from supermegazord.lib import ping, busy
from supermegazord.lib.machine import Machine

max_height = 24
max_width  = 80
max_namesize = 12

sections = []
statuses = {}
colors = None
counts = {
	'unknown': 0,
	'up': 0,
	'down': 0,
	'busy': 0
}

def mark_redraw():
	global redraw
	redraw = True

class ColorHolder:
	def __init__(self):
		curses.init_pair(1, curses.COLOR_GREEN,   curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_YELLOW,  curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_WHITE,   curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_RED,     curses.COLOR_BLACK)
		curses.init_pair(6, curses.COLOR_RED,     curses.COLOR_WHITE)

		self.GREEN   =      curses.color_pair(1)
		self.YELLOW  =      curses.color_pair(2)
		self.MAGENTA =      curses.color_pair(3)
		self.WHITE   =      curses.color_pair(4)
		self.RED     =      curses.color_pair(5)
		self.RED_ON_WHITE = curses.color_pair(6)

PORT = 10
BUFSIZ = 1024
class Status:
	machine = None
	usage_known = False
	usage_avaible = True
	network_known = False
	users = set()
	down = False
	def __init__(self, m):
		counts['unknown'] += 1
		self.machine = m

	def name_color(self):
		if not self.network_known:
			return colors.WHITE
		if self.usage_known and len(self.users) > 0:
			return colors.YELLOW
		return colors.RED_ON_WHITE if self.down else colors.GREEN

	def query_network(self):
		import subprocess
		val = subprocess.call("ping -c 1 -W 2 %s" % self.machine.hostname,
							  shell=True, stdout=open('/dev/null', 'w'),
							  stderr=subprocess.STDOUT)
		if self.network_known:
			counts['down' if self.down else 'up'] -= 1
		else:
			counts['unknown'] -= 1
		self.network_known = True
		self.down = (val != 0)
		counts['down' if self.down else 'up'] += 1
		mark_redraw()

	def query_usage(self):
		import socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((self.machine.hostname, PORT))
			sock.send("who")
			data = sock.recv(BUFSIZ)
			sock.close()
		except socket.error:
			data = None
			self.usage_avaible = False
		self.usage_known = True
		if data:
			if len(self.users) > 0: counts['busy'] -= 1
			self.users = set()
			for userinfo in data.split('\n'):
				self.users.add(userinfo.split(' ')[0])
			if len(self.users) > 0: counts['busy'] += 1
		mark_redraw()

class Section(collections.namedtuple("Section", "name machines")):
	def draw(self, screen):
		num_per_line = (max_width - 2) / (max_namesize + 1)
		num_lines    = 1 + (max(len(self.machines) - 1, 0)) / num_per_line
		total_width = min(num_per_line, len(self.machines)) * (max_namesize + 1)
		y, _ = screen.getyx()
		screen.addstr("╔═══" + self.name + ("═" * (total_width - len(self.name) - 3)) + "╗")
		ny, _ = screen.getyx()
		if y == ny: screen.addstr("\n")
		for line in range(num_lines):
			y, _ = screen.getyx()
			screen.addstr("║")
			count = 0
			for i in range(line * num_per_line, min((line+1)*num_per_line, len(self.machines))):
				status = statuses[self.machines[i].hostname]
				screen.addstr(" " if status.usage_avaible else "?", colors.MAGENTA)
				screen.addnstr(self.machines[i].hostname, max_namesize, status.name_color())
				rest = max_namesize - len(self.machines[i].hostname)
				if rest > 0:
					screen.addstr(" " * rest)
				count += 1
			if count * (max_namesize + 1) < total_width:
				screen.addstr(" " * (total_width - count * (max_namesize + 1)))
			screen.addstr("║")
			ny, _ = screen.getyx()
			if y == ny: screen.addstr("\n")
		y, _ = screen.getyx()
		screen.addstr("╚" + ("═" * total_width) + "╝")
		ny, _ = screen.getyx()
		if y == ny: screen.addstr("\n")
			

current_update = None
class UpdateJob:
	queue = None
	threads = []
	def __init__(self, data, num_threads = 32):
		from Queue import Queue
		from threading import Thread
		self.queue = Queue()
		for status in data.values():
			self.queue.put(status.query_network)
			self.queue.put(status.query_usage)
		for i in range(num_threads):
			worker = Thread(target=self.process)
			worker.daemon = True
			self.threads.append(worker)

	def start(self):
		for worker in self.threads:
			worker.start()

	def process(self):
		import Queue
		while True:
			try: value = self.queue.get()
			except Queue.Empty: return
			value()
			self.queue.task_done()

userquit = False
def signal_int(signalnum, handler):
	global userquit
	userquit = True

def fill_with_spaces(s, size, right_side = True):
    if right_side:
        return (str(s) + " " * size)[:size]
    else:
        return (" " * size + str(s))[-size:]

redraw = True
def draw(screen):
	screen.clear()
	for section in sections:
		section.draw(screen)
	screen.addstr("UNK:"   + fill_with_spaces(counts['unknown'], 2, False), colors.WHITE)
	screen.addstr(" UP: "  + fill_with_spaces(counts['up']     , 2, False), colors.GREEN)
	screen.addstr(" DOWN:" + fill_with_spaces(counts['down']   , 2, False), colors.RED)
	screen.addstr(" BUSY:" + fill_with_spaces(counts['busy']   , 2, False), colors.YELLOW)

# O wrapper impede que o terminal fique zuado caso de alguma merda no script
def main(screen):
	global userquit, redraw, max_height, max_width, colors, current_update
	curses.curs_set(0)
	screen.timeout(1)
	screen.notimeout(0)
	max_height, max_width = screen.getmaxyx()
	colors = ColorHolder()

	import supermegazord.db.machines as machines

	sections.append(Section("Servidores", machines.list("servidores")))
	sections.append(Section("122", machines.list("122")))
	sections.append(Section("125a", machines.list('125a')))
	sections.append(Section("125b", machines.list('125b')))
	sections.append(Section("126", machines.list('126')))
	sections.append(Section("258", machines.list('258')))
	sections.append(Section("Impressoras", machines.list('impressoras')))
	for section in sections:
		for m in section.machines:
			statuses[m.hostname] = Status(m)

	current_update = UpdateJob(statuses)
	current_update.start()

	userquit = False
	while not userquit:
		c = screen.getch()
		if c == curses.KEY_RESIZE:
			max_height, max_width = screen.getmaxyx()
			mark_redraw()
		elif c == ord('q'):
			userquit = True
		if redraw:
			redraw = False
			draw(screen)
		screen.refresh()

def Run():
	signal.signal(signal.SIGINT, signal_int)
	curses.wrapper(main)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		Run()
		sys.exit()
	else:
		import supermegazord.client.watchman_parser as watchman_parser
		import argparse
		parser = argparse.ArgumentParser(description='Watchman')
		watchman_parser.setup_parser(parser)
		args = parser.parse_args()
		args.func(args)
