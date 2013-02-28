#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Jupinfo: Estrutura de dados do jupinfo
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-02-29
# Modificado em: 2012-01-13 por henriquelima

import collections
class JupInfo(collections.namedtuple("JupInfo", "nid, nome, curso, ingresso")):
    def __str__(self):
        return "JupInfo: NID " + (" "*8 + str(self.nid))[-8:] + "; " + (str(self.curso) + " "*4)[:4] + (
            "; Ing ") + self.ingresso + "; Nome: " + self.nome


cache = {}
def _convert_row(row):
	data = row.strip().split(':')
	try:
		ingresso = data[3]
	except:
		ingresso = "n/a"
	return JupInfo(data[0], data[1], data[2], ingresso)

def _load_cache():
	if len(cache) > 0: return
	import supermegazord.db.path as path
	for source in "jup_info", "nojup_info":
		try:
			with open(path.MEGAZORD_DB + "/usuarios/jupiter/" + source) as f:
				for line in f:
					info = _convert_row(line)
					cache[info.nid] = info
		except IOError, e:
			pass
	
def from_nid(nid):
	_load_cache()
	try:
		return cache[nid]
	except KeyError:
		return None

def from_login(login):
	import supermegazord.lib.account as account
	acc = account.from_login(login)
	if acc and acc.nid:
		return from_nid(acc.nid)
	return None
