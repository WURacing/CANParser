import can_parser

class LogFileCANParser(can_parser.CANParser):

	def __init__(self, dbc_file, log_file):
		super().__init__(dbc_file)
		self.log_file = log_file

	def packets(self):
		