import socket
import time

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
				return Message(0).add_result('UDP', port)
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


# def get_open_udp_ports(self, udp_ports):
# 	open_udp = []
# 	udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
# 							  socket.IPPROTO_ICMP)
# 	icmp_sock.bind(('0.0.0.0', 10000))
# 	icmp_sock.settimeout(self.timeout)
# 	for port in udp_ports:
# 		for p in port:
# 			for tries in range(3):
# 				udp_sock.sendto(b'data', (self.ip_address, int(p)))
# 				try:
# 					icmp_sock.recv(100)
# 				except socket.timeout:
# 					open_udp.append(p)
# 					break
# 	if self.guess:
# 		for port in open_udp:
# 			proto = define_protocol(udp_sock, self.ip_address, int(port))
# 			print(f'UDP {port} {proto}')
# 	else:
# 		for port in open_udp:
# 			print(f'UDP {port}')
