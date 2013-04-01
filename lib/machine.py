# -*- coding: utf-8 -*-

# Machine: Fornece a classe machine, utilizada pelo script ping
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-17 por henriquelima

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()


class Machine:
	def __init__(self, hostname, ip, mac, parent):
		self.hostname = hostname
		self.ip = ip
		self.mac = mac
		self.parent = parent
		self.aliases = []

	def Draw(self):
		self.parent.Draw()

	def __repr__(self):
		return "Machine[hostname={0}]".format(self.hostname)

class Status:
	machine = None
	usage_known = False
	usage_avaible = True
	network_known = False
	users = set()
	down = False
	def __init__(self, m):
		self.machine = m

	def query_network(self):
		import subprocess, os
		val = subprocess.call("ping -c 1 -W 2 %s" % self.machine.hostname,
							  shell=True, stdout=open(os.devnull, 'w'),
							  stderr=subprocess.STDOUT)
		self.network_known = True
		self.down = (val != 0)

	def query_usage(self):
		import supermegazord.lib.stats as stats
		data = stats.query(self.machine, "who")
		self.users = set()
		self.usage_known = True
		if data == False:
			self.usage_avaible = False
		else:
			for userinfo in data.strip().split('\n'):
				x = userinfo.split(' ')[0]
				if len(x) > 0:
					self.users.add(x)


