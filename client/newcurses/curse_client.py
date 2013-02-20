#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Super Megazord 2: LDAP Edition
# Com suporte à UTF-8!

# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05
# Modificado em: 2011-08-05 por henriquelima

# Megazord global variables
import functools
import collections

# Variaveis globais importantes
quit = False
current_screen = None
max_height = 24
max_width = 80
KEY_ESCAPE = 27

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

class BaseScreen:
    def __init__(self):
        self.screen_name = "Tela Genérica"
        self.header = ""
        self.commands = collections.OrderedDict()

    def update(self, c):
        if c == curses.KEY_RESIZE: return True
        if c in self.commands:
            result = self.commands[c]['func'](c)
            if result != None:
                return result
            return True

    def draw(self, screen):
        megazord_header(screen, self.screen_name)
        screen.addnstr("\n" + self.header + " " * max_width, max_width)

class BaseListScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
        self.current_line = 0
        self.data = list()
        self.filtering = False
        self.filter_string = ""
        self.update_data()
        
        def select(): return self.select(self.data[self.current_line]) if len(self.data) > 0 else False
        def start_filtering(): self.filtering = True
        self.commands[curses.KEY_DOWN]  = { 'func': lambda c: self.change_line(self.current_line + 1) }
        self.commands[curses.KEY_UP]    = { 'func': lambda c: self.change_line(self.current_line - 1) }
        self.commands[curses.KEY_NPAGE] = { 'func': lambda c: self.change_line(self.current_line + self.page_size()) }
        self.commands[curses.KEY_PPAGE] = { 'func': lambda c: self.change_line(self.current_line - self.page_size()) }
        self.commands[KEY_ESCAPE]       = { 'func': lambda c: self.change_filter("") }
        self.commands[ord('\n')]        = { 'func': lambda c: select() }
        self.commands[ord('1')]         = self.commands[curses.KEY_UP]
        self.commands[ord('2')]         = self.commands[curses.KEY_DOWN]
        self.commands[curses.KEY_RIGHT] = self.commands[curses.KEY_NPAGE]
        self.commands[curses.KEY_LEFT]  = self.commands[curses.KEY_PPAGE]
        self.commands[ord('/')]         = { 'func': lambda c: start_filtering(), "description": "Busca" }
    
    def change_line(self, newline):
        self.current_line = max(0, min(newline, len(self.data) - 1))
    
    def change_filter(self, filterstr):
        self.filter_string = filterstr
        self.update_data()
        self.change_line(self.current_line)

    def update_data(self): pass
    
    def filter_addchar(self, c):
        if c == KEY_ESCAPE:
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
        return BaseScreen.update(self, c)
   
    def page_size(self): return 20

    def select(self, row): pass

    def draw_row(self, screen, row_data, y, x, selected = False): pass

    def draw(self, screen):
        BaseScreen.draw(self, screen)
        current_page = int(self.current_line / self.page_size())
        num_pages = int(len(self.data) / self.page_size())
        start, count, offset_y, offset_x = current_page * self.page_size(), self.page_size(), 2, 0
        start = max(start, 0)
        for i in range(start, min(start+count, len(self.data))):
            self.draw_row(screen, self.data[i], offset_y + (i % self.page_size()), offset_x, i == self.current_line)
        screen.addnstr(offset_y + count, offset_x, 
                       " " * 15 + "Page " + str(current_page + 1) + "/" + str(num_pages + 1), max_width)
        if self.filtering:
            screen.addnstr(offset_y + count + 1, offset_x, "/" + self.filter_string, max_width)
        else:
            screen.addstr("\n")
            def print_small_command_instruction(comm):
                if not 'description' in self.commands[comm]: return
                screen.addch(comm, colors.GREEN)
                screen.addstr(" - " + self.commands[comm]["description"] + "; ")
            map(print_small_command_instruction, self.commands)
        

class UserListScreen(BaseListScreen):
    def __init__(self):
        BaseListScreen.__init__(self)
        self.screen_name = "Lista de Usuários"
        self.header = fill_with_spaces("Login", 20) + "  " + fill_with_spaces("NID  ", 8, False) + "  Nome"

        self.commands[ord('q')] = { 'func': lambda c: change_screen(None) }
        if precadastro_screen:
            self.commands[ord('p')] = { 'description': "Pré-Cadastro", 'func': lambda c: change_screen(precadastro_screen) }

    def page_size(self):
        return max_height - 4
    
    def select(self, row):
        change_screen(UserInfoScreen(row))
        return True

    def update_data(self):
        import supermegazord.lib.account as account
        self.data = sorted(account.search(self.filter_string), key=lambda item: item.login)

    def draw_row(self, screen, user, y, x, selected):
        screen.addnstr(y, x,
            fill_with_spaces(user.login, 20) + "  " +
            fill_with_spaces(user.nid if user.nid else "n/a", 8, False) + "  " +
            fill_with_spaces(user.name, max_width),
            max_width, colors.YELLOW if selected else colors.WHITE)

class PrecadastroListScreen(BaseListScreen):
    def __init__(self):
        BaseListScreen.__init__(self)
        self.screen_name = "Lista de Pré-Cadastros"
        self.header = fill_with_spaces("Login", 20) + "  " + fill_with_spaces("NID  ", 8, False) + "  Nome"
        
        self.commands[ord('q')] = { 'func': lambda c: change_screen(None) }
        self.commands[ord('p')] = { 'func': lambda c: change_screen(userlist_screen), "description": "Lista de Usuários" }

    def page_size(self):
        return max_height - 4
        
    def update_data(self):
        import supermegazord.lib.precadastro as precadastro
        self.data = sorted(precadastro.list_all(), key=lambda item: item['login'])

    def draw_row(self, screen, user, y, x, selected):
        import supermegazord.lib.jupinfo as libjupinfo
        jupinfo = libjupinfo.from_nid(user['nid'])
        screen.addnstr(y, x,
            fill_with_spaces(user['login'], 20) + "  " +
            fill_with_spaces(user['nid'], 8, False) + "  " +
            fill_with_spaces(jupinfo and jupinfo.nome or "n/a", max_width),
            max_width, colors.YELLOW if selected else colors.WHITE)


class BaseInfoScreen(BaseScreen):
    def __init__(self):
        BaseScreen.__init__(self)
        self.screen_name = "Informações de Usuário"
        self.current = None
        self.queued_command = None
        self.command_output = None

    def update(self, c):
        if c == curses.KEY_RESIZE: return True
        
        if self.command_output:
            if c == ord('\n') or c == KEY_ESCAPE or c == ord('n'):
                self.command_output = self.queued_command = None
                return True
            elif c == ord('q'):
                self.commands[ord('q')]['func'](c)
                return True
            return False
        elif self.queued_command:
            if c == ord('y'):
                self.command_output = self.queued_command['execute']()
                return True
            elif c == ord('\n') or c == ord('q') or c == KEY_ESCAPE or c == ord('n'):
                self.queued_command = None
                return True
            return False
        return BaseScreen.update(self, c)
    
    def draw_current(self, screen): pass

    def draw(self, screen):
        BaseScreen.draw(self, screen)
        if self.current:
            self.draw_current(screen)

        screen.addstr("\n")
        if not self.queued_command:
            screen.addnstr("\n              Operações possíveis:", max_width)
            screen.addstr("\n")
            def print_command_instruction(data):
                key, comm = data
                if 'description' in comm:
                    screen.addstr("\n         '")
                    screen.addch(key, colors.GREEN)
                    screen.addstr("' para " + comm['description'] + ".")
                else:
                    screen.addstr("\n")
            map(print_command_instruction, self.commands.items())
        else:
            desc = self.queued_command['description'].upper() 
            screen.addnstr("\n              " + desc, max_width, colors.RED)
            screen.addstr("\n\n")
            if self.command_output:
                for s in self.command_output.split("\n"):
                    screen.addnstr(s, max_width)
            else:
                confirmstr = "Confirmar? (y/N)"
                screen.addnstr("              " + " " * ((len(desc) - len(confirmstr)) / 2) + confirmstr, max_width)

class UserInfoScreen(BaseInfoScreen):
    def __init__(self, user):
        BaseInfoScreen.__init__(self)
        self.current = user
        def confirm(c):
            self.queued_command = self.commands[c]
            if 'execute' not in self.queued_command:
                raise Exception("Command requesting confirmation has no execute attrib.")
        def nyi(c):
            self.queued_command = { 'description': "Não Implementado" }
            self.command_output = "Comando não implementado. Use a CLI."
        def nothing(): return "TMPSTRING"
        self.commands[ord('p')] = { 'description': "gerar uma nova senha", 'func': confirm, 'execute': nothing }
        self.commands[ord('d')] = { 'description': "desativar a conta",    'func': nyi, 'execute': nothing }
        self.commands[ord('r')] = { 'description': "reativar a conta",     'func': nyi, 'execute': nothing }
        self.commands[ord('a')] = { 'description': "apagar a conta",       'func': nyi, 'execute': nothing }
        self.commands[KEY_ESCAPE] = { 'func': lambda c: change_screen(userlist_screen) }
        self.commands[ord('q')] = { 'description': "voltar à tela anterior", 'func': lambda c: change_screen(userlist_screen) }

    def draw_current(self, screen):
        import supermegazord.lib.jupinfo as libjupinfo
        jupinfo = libjupinfo.from_nid(self.current.nid)
        screen.addnstr("\nLogin:    " + self.current.login, max_width)
        screen.addnstr("\nNome:     " + self.current.name, max_width)
        screen.addnstr("\nNID:      " + (self.current.nid or "n/a"), max_width)
        screen.addnstr("\nCurso:    " + self.current.group.name, max_width)
        screen.addnstr("\nIngresso: " + (jupinfo and jupinfo.ingresso or "n/a"), max_width)

#=======================
# Lista de telas
userlist_screen = None
precadastro_screen = None

def main(screen):
    #screen.nodelay(True)
    global max_height, max_width
    curses.curs_set(0)
    screen.timeout(1)
    screen.notimeout(0)
    max_height,max_width = screen.getmaxyx()

    colors.init()

    global current_screen, userlist_screen, precadastro_screen
    try: precadastro_screen = PrecadastroListScreen()
    except Exception, e: pass
    current_screen = userlist_screen = UserListScreen()

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
