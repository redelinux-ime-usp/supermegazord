#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Watchman: Monitora o estado das máquianas da rede.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-05 por henriquelima

import curses, sys, collections
import locale
locale.setlocale(locale.LC_ALL, '')

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

def status_color(status):
	if not status.network_known:
		return colors.WHITE
	if status.usage_known and len(status.users) > 0:
		return colors.YELLOW
	return colors.RED_ON_WHITE if status.down else colors.GREEN
	

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
				screen.addnstr(self.machines[i].hostname, max_namesize, status_color(status))
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
current_update = None
def main(screen):
	global redraw, max_height, max_width, colors, current_update
	curses.curs_set(0)
	screen.timeout(1)
	screen.notimeout(0)
	max_height, max_width = screen.getmaxyx()
	colors = ColorHolder()

	import supermegazord.db.machines as machines
	import supermegazord.lib.machine as machine
	sections.append(Section("Servidores", sorted(machines.list("servidores"), key=lambda m: m.hostname)))
	sections.append(Section("122" , sorted(machines.list("122" ), key=lambda m: m.hostname)))
	sections.append(Section("125a", sorted(machines.list('125a'), key=lambda m: m.hostname)))
	sections.append(Section("125b", sorted(machines.list('125b'), key=lambda m: m.hostname)))
	sections.append(Section("126" , sorted(machines.list('126' ), key=lambda m: m.hostname)))
	sections.append(Section("258" , sorted(machines.list('258' ), key=lambda m: m.hostname)))
	sections.append(Section("Impressoras", sorted(machines.list('impressoras'), key=lambda m: m.hostname)))
	for section in sections:
		for m in section.machines:
			statuses[m.hostname] = machine.Status(m)
			counts['unknown'] += 1

	import supermegazord.lib.worker as worker
	current_update = worker.Processor()
	def network(status):
		if status.network_known:
			counts['down' if status.down else 'up'] -= 1
		else:
			counts['unknown'] -= 1
		status.query_network()
		counts['down' if status.down else 'up'] += 1
		mark_redraw()
	def usage(status):
		counts['busy'] -= min(len(status.users), 1)
		status.query_usage()
		counts['busy'] += min(len(status.users), 1)
		mark_redraw()
	for status in statuses.values():
		current_update.add_job((network, status))
		current_update.add_job((usage, status))
	current_update.start()

	userquit = False
	while not userquit:
		try:
			c = screen.getch()
		except KeyboardInterrupt:
			c = ord('q')
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
