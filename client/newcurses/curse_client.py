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
max_height = 24
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

def change_screen(newscreen):
    global current_screen
    current_screen = newscreen

class BaseListScreen:
    def __init__(self):
        self.current_line = 0
        self.data = list()
        self.screen_name = "Lista Genérica"
        self.header = ""
        self.filtering = False
        self.filter_string = ""
        
        def select(): return self.select(self.data[self.current_line]) if len(self.data) > 0 else False
        def start_filtering(): self.filtering = True
        self.commands = {
            curses.KEY_DOWN:  lambda c: self.change_line(self.current_line + 1),
            curses.KEY_UP:    lambda c: self.change_line(self.current_line - 1),
            curses.KEY_NPAGE: lambda c: self.change_line(self.current_line + self.page_size()),
            curses.KEY_PPAGE: lambda c: self.change_line(self.current_line - self.page_size()),
            27:               lambda c: self.change_filter(""),
            ord('/'):         lambda c: start_filtering(),
            ord('\n'):        lambda c: select()
        }
        self.commands[ord('1')] = self.commands[curses.KEY_UP]
        self.commands[ord('2')] = self.commands[curses.KEY_DOWN]
        self.commands[curses.KEY_RIGHT] = self.commands[curses.KEY_NPAGE]
        self.commands[curses.KEY_LEFT]  = self.commands[curses.KEY_PPAGE]
    
    def change_line(self, newline):
        self.current_line = max(0, min(newline, len(self.data) - 1))
    
    def change_filter(self, filterstr):
        self.filter_string = filterstr
        self.update_data()
        self.change_line(self.current_line)

    def update_data(self): pass
    
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
        self.update_data()
        self.change_line(self.current_line)
        return True

    def update(self, c):
        if c == curses.KEY_RESIZE: return True
        if self.filtering:
            return self.filter_addchar(c)
        if c in self.commands:
            result = self.commands[c](c)
            if result != None:
                return result
            return True
   
    def page_size(self): return 20

    def select(self, row): pass

    def draw_row(self, screen, row_data, y, x, selected = False): pass

    def draw(self, screen):
        current_page = int(self.current_line / self.page_size())
        num_pages = int(len(self.data) / self.page_size())
        start, count, offset_y, offset_x = current_page * self.page_size(), self.page_size(), 2, 0
        start = max(start, 0)
        megazord_header(screen, self.screen_name)
        screen.addnstr("\n" + self.header + " " * max_width, max_width)
        for i in range(start, min(start+count, len(self.data))):
            self.draw_row(screen, self.data[i], offset_y + (i % self.page_size()), offset_x, i == self.current_line)
        screen.addnstr(offset_y + count, offset_x, 
                       " " * 15 + "Page " + str(current_page + 1) + "/" + str(num_pages + 1), max_width)
        if self.filtering:
            screen.addnstr(offset_y + count + 1, offset_x, "/" + self.filter_string, max_width)
        else:
            screen.addstr("\n")
            def print_small_command_instruction(key, description):
                screen.addch(ord(key), colors.GREEN)
                screen.addstr(" - " + description + "; ")
            print_small_command_instruction('/', "Busca")
            print_small_command_instruction('p', "Pré-Cadastro")
        

class UserListScreen(BaseListScreen):
    def __init__(self):
        BaseListScreen.__init__(self)
        self.filtering = False
        self.filter_string = ""
        self.update_data()
        self.screen_name = "Lista de Usuários"
        self.header = fill_with_spaces("Login", 20+2) + fill_with_spaces("Grupo", 9) + "Nome"

        self.commands[ord('q')] = lambda c: change_screen(None)
        self.commands[ord('p')] = lambda c: change_screen(precadastro_screen)

    def page_size(self):
        return max_height - 4
    
    def select(self, row):
        userinfo_screen.current_user = row
        change_screen(userinfo_screen)
        return True

    def update_data(self):
        import supermegazord.lib.account as account
        self.data = sorted(account.search(self.filter_string), key=lambda item: item.login)

    def draw_row(self, screen, user, y, x, selected):
        screen.addnstr(y, x,
            fill_with_spaces(user.login, 20) + "  " +
            fill_with_spaces(user.group.name, 7) + "  " +
            fill_with_spaces(user.name, max_width),
            max_width, colors.YELLOW if selected else colors.WHITE)

class UserInfoScreen:
    def __init__(self):
        self.current_user = None

    def update(self, c):
        global current_screen
        if c == ord('q') or c == 27:
            current_screen = userlist_screen
            return True
        return False

    def draw(self, screen):
        import supermegazord.lib.jupinfo as libjupinfo
        jupinfo = libjupinfo.from_nid(self.current_user.nid)
        megazord_header(screen, "Informações de Usuário")
        screen.addstr("\n")
        screen.addnstr("\nLogin:    " + self.current_user.login, max_width)
        screen.addnstr("\nNome:     " + self.current_user.name, max_width)
        screen.addnstr("\nNID:      " + self.current_user.nid, max_width)
        screen.addnstr("\nCurso:    " + self.current_user.group.name, max_width)
        screen.addnstr("\nIngresso: " + (str(jupinfo.ingresso) if jupinfo else "n/a"), max_width)
        screen.addstr("\n")
        screen.addnstr("\n              Operações possíveis:", max_width)
        screen.addstr("\n")

        def print_command_instruction(key, description):
            screen.addstr("\n         '")
            screen.addch(ord(key), colors.GREEN)
            screen.addstr("' para " + description + ".")
            

        print_command_instruction('p', "gerar uma nova senha")
        print_command_instruction('d', "desativar a conta")
        print_command_instruction('r', "reativar a conta")
        screen.addstr("\n")
        print_command_instruction('q', "voltar à tela anterior")

class PrecadastroListScreen:
    def __init__(self):
        self.current_line = 0
        self.page_size = max_height - 4
        self.filtering = False
        self.filter_string = ""
        self.update_filter()
        pass

    def change_line(self, newline):
        self.current_line = max(0, min(newline, len(self.users) - 1))

    def update_filter(self):
        import supermegazord.lib.precadastro as precadastro
        self.users = sorted(precadastro.list_all(), key=lambda item: item['login'])
        self.change_line(self.current_line)

    def filter_addchar(self, c):
        self.filtering = False
        self.update_filter()
        return True

    def update(self, c):
        global current_screen
        if c == curses.KEY_RESIZE:
            self.page_size = max_height - 4
            return True

        if self.filtering:
            return self.filter_addchar(c)
        if c == ord('q'):
            current_screen = None
        elif c == 27:
            self.filter_string = ""
            self.update_filter()
            return True
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
        elif c == ord('\n'):
            if len(self.users) > 0:
                current_screen = None
            return True
        return False

    def draw(self, screen):
        current_page = int(self.current_line / self.page_size)
        num_pages = int(len(self.users) / self.page_size)
        start, count, offset_y, offset_x = current_page * self.page_size, self.page_size, 2, 0
        start = max(start, 0)
        megazord_header(screen, "Lista de Pré-Cadastros")
        screen.addnstr("\n" + fill_with_spaces("Login", 12+2) + fill_with_spaces("NID", 9), max_width)
        for i in range(start, min(start+count, len(self.users))):
            screen.addnstr(offset_y + (i % self.page_size), offset_x,
                fill_with_spaces(self.users[i]['login'], 12) + "  " + fill_with_spaces(self.users[i]['nid'], 7),
                max_width, colors.YELLOW if i == self.current_line else colors.WHITE)
        screen.addnstr(offset_y + count, offset_x, " " * 15 + "Page " + str(current_page + 1) + "/" + str(num_pages + 1), max_width)
        if self.filtering:
            screen.addnstr(offset_y + count + 1, offset_x, "/" + self.filter_string, max_width)
        else:
            screen.addstr("\n")
            def print_small_command_instruction(key, description):
                screen.addch(ord(key), colors.GREEN)
                screen.addstr(" - " + description + "; ")
            print_small_command_instruction('/', "Busca")
            print_small_command_instruction('p', "Usuários")

#=======================
# Lista de telas
userlist_screen = None
userinfo_screen = None
precadastro_screen = None

def main(screen):
    #screen.nodelay(True)
    global max_height, max_width
    curses.curs_set(0)
    screen.timeout(1)
    screen.notimeout(0)
    max_height,max_width = screen.getmaxyx()

    colors.init()

    global current_screen, userlist_screen, userinfo_screen
    current_screen = userlist_screen = UserListScreen()
    userinfo_screen = UserInfoScreen()
    precadastro_screen = PrecadastroListScreen()

    redraw = True
    while current_screen:
        if redraw:
            screen.clear()
            current_screen.draw(screen)
        try:
            c = screen.getch()
        except KeyboardInterrupt:
            break
        if c == curses.KEY_RESIZE:
            max_height,max_width = screen.getmaxyx()
        redraw = current_screen.update(c)
        screen.refresh()

def Run():
    curses.wrapper(main)

if __name__ == "__main__":
    Run()
