# -*- coding: utf-8 -*-

# Threads: Chama uma função para todos os elementos da lista, paralelamente.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2011-08-22
# Modificado em: 2011-08-22 por henriquelima

from threading import Thread
from Queue import Queue

num_threads = 16
queue = Queue()

def Worker(i, q):
	while True:
		value = q.get()
		value[1](value[0])
		q.task_done()


def Run(work, group):
	#Spawn thread pool
	for i in range(num_threads):
		worker = Thread(target=Worker, args=(i, queue))
		worker.setDaemon(True)
		worker.start()

	#Place work in ping_queue
	for member in group:
		t = member, work
		queue.put(t)

def Wait():
	#Wait until worker threads are done to exit    
	queue.join()

def Idle():
	return len(queue) == 0

