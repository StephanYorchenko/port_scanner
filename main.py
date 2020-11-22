import argparse
import sys

from Manager import Manager

srange = lambda x, y: range(x, y + 1)


class CLInterface:
	def __init__(self, manager):
		self.manager = manager

	@staticmethod
	def get_input_parameters():
		parser = argparse.ArgumentParser(
				description="Cканер TCP и UDP портов"
		)
		parser.add_argument("ip_address", type=str, help="ip address")
		parser.add_argument(
				"--timeout",
				type=int,
				default=2,
				help="таймаут ожидания ответа (по умолчанию 2с)",
		)
		parser.add_argument(
				'-j', '--num-threads', default=1, type=int,
				help="число потоков"
		)
		parser.add_argument(
				'-v', '--verbose', action="store_true", help="подробный режим"
		)
		parser.add_argument('-g', '--guess', action="store_true")
		parser.add_argument('ports', metavar='PORT', type=str, nargs='+',
							help='ports....')
		return parser.parse_args()

	@classmethod
	def initialize(cls):
		input_args = CLInterface.get_input_parameters()
		manager = Manager(*CLInterface.parse_parameters(input_args))
		return cls(manager)

	@staticmethod
	def parse_parameters(inputted_args):
		yield inputted_args.ip_address
		ports = {'tcp': set(), 'udp': set()}
		for arg in inputted_args.ports:
			protocol = arg[:3]
			if len(arg) == 3:
				ports[protocol].update(set(range(1, 2 ** 16)))
				continue
			arg = arg[4:]
			_ports = set()
			for chunk in arg.split(','):
				if '-' in chunk:
					_ports.update(set(srange(*map(int, chunk.split('-')))))
				else:
					_ports.add(int(chunk))
			ports[protocol].update(_ports)
		yield {k: sorted(list(v)) for k, v in ports.items()}
		yield inputted_args.timeout
		yield inputted_args.verbose
		yield inputted_args.num_threads
		yield inputted_args.guess

	@staticmethod
	def show(row) -> None:
		print(row)

	def sigint_handler(self, signal, frame):
		CLInterface.show(self.manager.results)
		sys.exit(0)

	def start(self):
		self.manager.start()
		for i in self.manager.get_output():
			self.show(i)

	@staticmethod
	def catch_error(message):
		CLInterface.show(message)
		sys.exit(message.value)


if __name__ == "__main__":
	a = CLInterface.initialize()
	a.start()
