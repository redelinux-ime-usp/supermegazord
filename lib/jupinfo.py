#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Jupinfo: Estrutura de dados do jupinfo
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-02-29
# Modificado em: 2012-01-13 por henriquelima

class JupInfo:
	def __init__(self, nid, nome, curso, ingresso):
		self.nid = nid
		self.nome = nome
		self.curso = curso
		self.ingresso = ingresso

	def __str__(self):
		return "NID:" + (" "*8 + str(self.nid))[-8:] + " Curso: " + (str(self.curso) + " "*4)[:4] + (
			" Ingresso: ") + self.ingresso + "; Nome: " + self.nome

	def __repr__(self):
		return "JupInfo('%s','%s','%s','%s')" % (self.nid, self.nome, self.curso, self.ingresso)
