import random
import socket
import struct
import time

from message import Message


class TCPWorker:
	def __init__(self, host: str, timeout: int):
		self.ip_addr = host
		self.timeout = timeout

	def _scan_port(self, sock, port):
		try:
			start = time.time()
			sock.connect((self.ip_addr, port))
			result = time.time() - start
			result = round(result, 3) * 1000
		except socket.timeout:
			return Message(1).add_result('Closed')
		except ConnectionRefusedError:
			return Message(1).add_result('Closed')

		prot = self.define_tcp_protocol(sock)
		return Message(0).add_result('TCP', port, result, prot)

	def scan(self, port) -> Message:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(self.timeout)
		a = self._scan_port(sock, port)
		sock.close()
		return a

	def define_tcp_protocol(self, sock):
		requests, ID = self.get_requests()
		for request in requests.values():
			sock.send(request)
			try:
				data = sock.recv(2048)
				if data is not None:
					proto = self.define_answer_type(data, ID, request)
					return proto
			except socket.timeout:
				pass
		return "-"

	@staticmethod
	def get_requests():
		id = random.randint(1, 65535)
		requests = {'HTTP': b'GET / HTTP/1.1',
					'DNS': struct.pack("!HHHHHH", id, 256, 1, 0, 0, 0)
						   + b"\x06google\x03com\x00\x00\x01\x00\x01",
					'ECHO': b'hello'}
		return requests, id

	@staticmethod
	def define_answer_type(data, id, sended_data):
		if data[:4].startswith(b'HTTP'):
			return 'HTTP'
		elif struct.pack('!H', id) in data:
			return 'DNS'
		elif data == sended_data:
			return 'ECHO'
		return '-'
