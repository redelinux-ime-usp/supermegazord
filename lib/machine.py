# -*- coding: utf-8 -*-

# Machine: Fornece a classe machine, utilizada pelo script ping
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-05 
# Modificado em: 2011-08-17 por henriquelima

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()


class Machine:
	def __init__(self, hostname, parent):
		self.hostname = hostname
		self.parent = parent
		self.ResetStatus()


	def Draw(self):
		self.parent.Draw()

	def Color(self):
		result = 0
		if self.QueryFinished() == False:
			result = 0
		elif self.Power() == False:
			result = 2
		elif self.UserList() != []:
			result = 3
		else:
			result = 1	
		return self.parent.Colors(result)

	# Getters
	def Name(self):
		return self.hostname

	def QueryFinished(self):
		return self.query_finished
	
	def Power(self):
		return self.power

	def StatsAvaiable(self):
		return self.stats_avaiable

	def UserList(self):
		return self.user_list

	# Setters
	def FinishQuery(self):
		self.query_finished = True

	def SetPower(self, power):
		self.power = power

	def SetStatsAvaiability(self, status):
		self.stats_avaiable = status

	def SetUserList(self, users):
		self.user_list = users

	def ResetStatus(self):
		self.query_finished = False
		self.power = True
		self.stats_avaiable = True
		self.user_list = []
