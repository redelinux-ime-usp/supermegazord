#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# cria_dns: Gera o arquivo de dns baseado na db de máquinas da rede.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-08-31

import supermegazord.db.machines as machines
from supermegazord.lib.machine import Machine

data = ""
for m in machines.list('all'):
	data += m.hostname + " A " + m.ip + "\n"
	for alias in m.aliases:
		data += alias + " CNAME " + m.hostname + "\n"

import subprocess
p = subprocess.Popen(['ssh', 'megazord@dns', 'sudo /etc/bind/redelinux/update-dns'], shell=False, stdin=subprocess.PIPE)
p.communicate(data)
