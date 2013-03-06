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
MAX_NAMESIZE = 12

sections = []
statuses = {}
colors = None

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

def addstr_newline(screen, s):
	y, _ = screen.getyx()
	screen.addstr(s)
	ny, _ = screen.getyx()
	if y == ny: screen.addstr("\n")

class Section(collections.namedtuple("Section", "name machines")):
	def draw_header(self, screen, width):
		header = (u"═" * width)
		header = header[:3] + self.name.decode("UTF-8") + header[4:]
		header = u"╔" + header[0:width] + u"╗"
		addstr_newline(screen, header.encode("UTF-8"))

	def draw_item(self, screen, item):
		status = statuses[item.hostname]
		screen.addstr(" " if status.usage_avaible else "?", colors.MAGENTA)
		screen.addnstr(item.hostname, MAX_NAMESIZE, status_color(status))
		rest = MAX_NAMESIZE - len(item.hostname)
		if rest > 0:
			screen.addstr(" " * rest)

	def draw(self, screen):
		num_per_line = (max_width - 2) / (MAX_NAMESIZE + 1)
		num_lines    = 1 + (max(len(self.machines) - 1, 0)) / num_per_line
		total_width = min(num_per_line, len(self.machines)) * (MAX_NAMESIZE + 1)
		self.draw_header(screen, total_width)
		for line in range(num_lines):
			y, _ = screen.getyx()
			screen.addstr("║")
			count = min((line+1)*num_per_line, len(self.machines)) - (line * num_per_line)
			for i in range(line * num_per_line, line * num_per_line + count):
				self.draw_item(screen, self.machines[i])
			if count * (MAX_NAMESIZE + 1) < total_width:
				screen.addstr(" " * (total_width - count * (MAX_NAMESIZE + 1)))
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
		try:
			section.draw(screen)
		except curses.error:
			return
	try:
		counts = {
			'unknown': len(filter(lambda x: not x.network_known, statuses.values())),
			'up': len(filter(lambda x: x.network_known and not x.down, statuses.values())),
			'down': len(filter(lambda x: x.network_known and x.down, statuses.values())),
			'busy': len(filter(lambda x: len(x.users) > 0, statuses.values()))
		}
		screen.addstr("UNK:"   + fill_with_spaces(counts['unknown'], 2, False), colors.WHITE)
		screen.addstr(" UP: "  + fill_with_spaces(counts['up']     , 2, False), colors.GREEN)
		screen.addstr(" DOWN:" + fill_with_spaces(counts['down']   , 2, False), colors.RED)
		screen.addstr(" BUSY:" + fill_with_spaces(counts['busy']   , 2, False), colors.YELLOW)
	except curses.error:
		return

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

	import supermegazord.lib.worker as worker
	current_update = worker.Processor()
	def network(status):
		status.query_network()
		mark_redraw()
	def usage(status):
		status.query_usage()
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
