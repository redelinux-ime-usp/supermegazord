#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05
# Modificado em: 2011-08-05 por henriquelima

# Megazord global variables
import functools

# Variaveis globais importantes
quit = False
current_screen = None
max_width = 80

import curses, curses.textpad
import supermegazord.base.colors as colors

def fill_with_spaces(s, size, right_side = True):
    if right_side:
        return (s + " " * size)[:size]
    else:
        return (" " * size + s)[-size:]

def megazord_header(screen, section):
    screen.addnstr(" " * 10 + "SUPERMEGAZORD - " + section + " " * max_width, max_width)

class UserListScreen:
    def __init__(self):
        self.current_line = 0
        self.page_size = 20
        self.filtering = False
        self.filter_string = ""
        self.update_filter()
        pass

    def change_line(self, newline):
        self.current_line = max(0, min(newline, len(self.users) - 1))

    def update_filter(self):
        import supermegazord.lib.account as account
        self.users = sorted(account.search(self.filter_string), key=lambda item: item.login)
        self.change_line(self.current_line)

    def filter_addchar(self, c):
        if c == 27:
            self.filtering = False
            self.filter_string = ""
        elif c == ord('\n'):
            self.filtering = False
        elif c >= ord('a') and c <= ord('z'):
            self.filter_string += chr(c)
        elif c == curses.KEY_BACKSPACE:
            if len(self.filter_string) > 0:
                self.filter_string = self.filter_string[:-1]
            else:
                self.filtering = False
        else:
            return False
        self.update_filter()
        return True

    def update(self, c):
        global current_screen
        if self.filtering:
            return self.filter_addchar(c)
        if c == ord('q'):
            current_screen = None
        elif c == ord('/'):
            self.filtering = True
            return True
        elif c == curses.KEY_DOWN or c == ord('2'):
            self.change_line(self.current_line + 1)
            return True
        elif c == curses.KEY_UP or c == ord('1'):
            self.change_line(self.current_line - 1)
            return True
        elif c == curses.KEY_RIGHT or c == curses.KEY_NPAGE: # Page Down
            self.change_line(self.current_line + self.page_size)
            return True
        elif c == curses.KEY_LEFT or c == curses.KEY_PPAGE: # Page Up
            self.change_line(self.current_line - self.page_size)
            return True
        elif c == curses.KEY_END:
            return True
        elif c == curses.KEY_HOME:
            return True
        elif c == ord('\n'):
            current_screen = userinfo_screen
            userinfo_screen.current_user = self.users[self.current_line]
            return True
        return False

    def draw(self, screen):
        current_page = int(self.current_line / self.page_size)
        num_pages = int(len(self.users) / self.page_size)
        start, count, offset_y, offset_x = current_page * self.page_size, self.page_size, 2, 0
        start = max(start, 0)
        megazord_header(screen, "Lista de Usuários")
        screen.addnstr("\n" + fill_with_spaces("Login", 20+2) + fill_with_spaces("Grupo", 7), max_width)
        for i in range(start, min(start+count, len(self.users))):
            screen.addnstr(offset_y + (i % self.page_size), offset_x,
                fill_with_spaces(self.users[i].login, 20) + "  " + fill_with_spaces(self.users[i].group.name, 7),
                max_width, colors.YELLOW if i == self.current_line else colors.WHITE)
        screen.addnstr(offset_y + count, offset_x, " " * 15 + "Page " + str(current_page + 1) + "/" + str(num_pages + 1), max_width)
        if self.filtering:
           screen.addnstr(offset_y + count + 1, offset_x, "/" + self.filter_string, max_width)

class UserInfoScreen:
    def __init__(self):
        self.current_user = None

    def update(self, c):
        global current_screen
        if c == ord('q'):
            current_screen = None
        elif c == 27:
            current_screen = userlist_screen
            return True
        elif c >= ord('a') and c <= ord('z'):
            print chr(c)
        return False

    def draw(self, screen):
        import supermegazord.lib.jupinfo as libjupinfo
        jupinfo = libjupinfo.from_nid(self.current_user.nid)
        megazord_header(screen, "Informações de Usuário")
        screen.addstr("\n")
        screen.addnstr("\nLogin:    " + self.current_user.login, max_width)
        screen.addnstr("\nNID:      " + self.current_user.nid, max_width)
        screen.addnstr("\nCurso:    " + self.current_user.group.name, max_width)
        screen.addnstr("\nIngresso: " + jupinfo.ingresso, max_width)
        screen.addnstr("\nNome:     " + self.current_user.name, max_width)

#=======================
# Lista de telas
userlist_screen = None
userinfo_screen = None

def main(screen):
    #screen.nodelay(True)
    curses.curs_set(0)
    screen.timeout(1)
    screen.notimeout(0)

    colors.init()

    redraw = True
    while current_screen:
        if redraw:
            screen.clear()
            current_screen.draw(screen)
        try:
            c = screen.getch()
        except KeyboardInterrupt:
            break
        redraw = current_screen.update(c)
        screen.refresh()

def Run():
    global current_screen, userlist_screen, userinfo_screen
    current_screen = userlist_screen = UserListScreen()
    userinfo_screen = UserInfoScreen()
    curses.wrapper(main)

if __name__ == "__main__":
    Run()
