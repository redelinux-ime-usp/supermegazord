# -*- coding: utf-8 -*-

# Worker: Processa uma lista de tarefas em paralelo.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2013-03-06

class Processor:
	queue = None
	threads = []
	def __init__(self, num_threads = 32):
		from Queue import Queue
		from threading import Thread
		self.queue = Queue()
		for i in range(num_threads):
			worker = Thread(target=self.process)
			worker.daemon = True
			self.threads.append(worker)

	def add_job(self, data):
		self.queue.put(tuple(data))

	def start(self):
		for worker in self.threads:
			worker.start()

	def process(self):
		import Queue
		while True:
			try: value = self.queue.get()
			except Queue.Empty: return
			value[0](*value[1:])
			self.queue.task_done()
