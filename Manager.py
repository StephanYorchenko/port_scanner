import socket
from collections import deque
from queue import Queue
from threading import Thread

from port import Port
from tcp_worker import TCPWorker
from udp_worker import UDPWorker


class myThread(Thread):
	def __init__(self, manager):
		Thread.__init__(self)
		self.manager = manager

	def run(self):
		while True:
			if self.manager.ports.empty():
				break
			port = self.manager.ports.get_nowait()
			a = self.manager.scan(port)
			if not a.code:
				self.manager.output.append(a)


class Manager:
	def __init__(self, host, ports: dict, timeout, verbose, num_threads, guess):
		self.guess = guess
		self.verbose = verbose
		self.host = socket.gethostbyname(host)
		self.ports = Queue()
		for p in [Port(v, k) for k, vv in ports.items() for v in vv]:
			self.ports.put(p)
		self.timeout = timeout
		self.tcp_worker = TCPWorker(self.host, self.timeout)
		self.num_threads = num_threads
		self.output = deque()
		self.udp_worker = UDPWorker(self.host, self.timeout)

	def scan(self, port):
		if port.protcol == 'tcp':
			return self.tcp_worker.scan(port.port)
		else:
			return self.udp_worker.scan(port.port)

	def start(self):
		a = []
		for i in range(self.num_threads):
			t = myThread(self)
			a.append(t)
			t.start()
		for i in a:
			i.join()

	def get_output(self):
		while True:
			if not self.output:
				break
			yield self.output.pop().output(self.verbose, self.guess)
