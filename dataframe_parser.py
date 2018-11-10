import canparser
import re

class DataFrameCANParser(canparser.CANParser):

	def __init__(self, dbc_file, dataframe):
		super().__init__(dbc_file)
		self.dataframe = dataframe

	def packets(self):
		for index, row in dataframe.iterrows():
			timestamp = int(row['timestamp'])
			msg_id = int(row['msg_id'], 16)
			data = bytes.fromhex(row['data'])

			#Epoch and extended are assumed for now
			packet = {
				'timestamp': timestamp,
				'epoch': False,
				'extended': True,
				'msg_id': msg_id,
				'data': data
			}

			yield packet