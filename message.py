class Message:
	def __init__(self, code):
		self.code = code
		self.result = []

	def add_result(self, *args):
		self.result += args
		return self

	def output(self, v=False, g=False) -> str:
		out = f'{self.result[0]} {self.result[1]}'
		if v and self.result[0] == 'tcp' or ( self.result[0] == 'udp' and g):
			out += ' ' + str(self.result[2])
		if g and self.result[0] == 'tcp':
			out += ' ' + str(self.result[3])
		return out
