# -*- coding: utf-8 -*-

# Cores: Fornece variaveis para colorir um terminal
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-09-29

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

pret = "\033[1;30m";
verm = "\033[1;31m";
verd = "\033[1;32m";
amar = "\033[1;33m";
azul = "\033[1;34m";
roxo = "\033[1;35m";
cian = "\033[1;36m";
norm = "\033[0m";

allcolors = { 'pret': pret, 'verm': verm, 'verd': verd, 'amar': amar, 'azul': azul, 'roxo': roxo, 'cian': cian, 'norm': norm }

def parse(s):
	return s % allcolors
