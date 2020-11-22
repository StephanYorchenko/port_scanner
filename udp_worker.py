import socket
import struct
from random import randint

from message import Message


class UDPWorker:
	def __init__(self, host: str, timeout: int):
		self.ip_addr = host
		self.timeout = timeout

	def _scan_port(self, udp_sock, icmp_sock, port):
		for tries in range(3):
			udp_sock.sendto(b'data', (self.ip_addr, port))
			try:
				icmp_sock.recv(100)
			except socket.timeout:
				prot = self.define_udp_protocol(udp_sock, port)
				return Message(0).add_result('UDP', port, prot)
		return Message(1).add_result('Closed')

	def scan(self, port) -> Message:
		udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
								  socket.IPPROTO_ICMP)
		icmp_sock.bind(('0.0.0.0', 10000))
		icmp_sock.settimeout(self.timeout)
		a = self._scan_port(udp_sock, icmp_sock, port)
		icmp_sock.close()
		udp_sock.close()
		return a

	def define_udp_protocol(self, sock, port):
		requests, ID = self.get_requests()
		for request_type in requests.keys():
			sock.settimeout(self.timeout)
			sock.sendto(requests[request_type], (self.ip_addr, port))
			try:
				data = sock.recv(2048)
				if data is not None:
					proto = self.define_answer_type(data, ID,
											   requests[request_type])
					return proto
			except socket.timeout:
				pass
		return '-'

	@staticmethod
	def define_answer_type(data, ID, sended_data):
		if data[:4].startswith(b'HTTP'):
			return 'HTTP'
		elif struct.pack('!H', ID) in data:
			return 'DNS'
		elif data == sended_data:
			return 'ECHO'
		else:
			return '-'

	@staticmethod
	def get_requests():
		id = randint(1, 65535)
		dns_request = struct.pack("!HHHHHH", id, 256, 1, 0, 0, 0) + b"\x06google\x03com\x00\x00\x01\x00\x01"
		requests = {
				'HTTP': b'GET / HTTP/1.1',
				'DNS': dns_request,
				'ECHO': b'hello'
		}
		return requests, id

