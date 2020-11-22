import socket
import time
from collections import deque

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
		except socket.timeout:
			return Message(1).add_result('Closed')
		except ConnectionRefusedError:
			return Message(1).add_result('Closed')
		return Message(0).add_result('TCP', port, result)

	def scan(self, port) -> Message:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(self.timeout)
		a = self._scan_port(sock, port)
		sock.shutdown(0)
		return a
