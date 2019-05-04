import abc
import cantools
import schema

"""
I'm not sure I will actually use these objects anywhere,
but provide them for the sake of having the schema described
in the code. Maybe these should be classes instead?
There's a feature in python 3.7 called 'dataclass' that does
exactly what I want, but I'm hesitant to use it because it's
so new.
"""
packet_schema = schema.Schema({
	'timestamp': int,
	'epoch': bool,
	'extended': bool,
	'msg_id': int,
	'data': bytes
})
signal_schema = schema.Schema({
	'timestamp': int,
	'epoch': bool,
	'sender': str,
	'msg_name': str,
	'sig_name': str,
	'sig_val': float,
	'units': str
})
"""
Purposefully contains some redundant info that should
be identical in every signal
"""
message_schema = schema.Schema({
	'timestamp': int,
	'epoch': bool,
	'sender': str,
	'msg_name': str,
	'msg_id': int,
	'signals': [signal_schema]
})

class CANParser(abc.ABC):

	def __init__(self, dbc_file):
		self.dbc_file = dbc_file
		self.db = cantools.database.load_file(self.dbc_file)

	"""
	We could memoize- but these lists don't typically get 
	longer than ~8; doesn't seem worth it
	"""
	def __get_units_from_signals(self, signals, sig_name):
		for signal in signals:
			if signal.name == sig_name:
				return signal.unit

	"""
	All subclasses must provide their own implementation
	Returns a generator over objects matching the 'packet' schema
	"""
	@abc.abstractmethod
	def packets(self):
		pass

	def messages(self):
		for packet in self.packets():
			msg = {
				'timestamp': packet['timestamp'],
				'epoch': packet['epoch'],
				'msg_id': packet['msg_id']
			}
			try:
				msg_inf = self.db.get_message_by_frame_id(msg['msg_id'])
			except KeyError:
				print(f"Missing {msg['msg_id']} in DBC")
				continue
			msg['msg_name'] = msg_inf.name
			"""
			I am choosing to assume that all messages will have only one sender
			I do not see this changing on our bus any time soon, but make note
			of this line if it does
			"""
			msg['sender'] = msg_inf.senders[0]
			msg['signals'] = []
			signals = self.db.decode_message(msg_inf.frame_id, packet['data'])
			for sig_name, sig_val in signals.items():
				signal = {
					'timestamp': msg['timestamp'],
					'epoch': msg['epoch'],
					'sender': msg['sender'],
					'msg_name': msg_inf.name,
					'sig_name': sig_name,
					'sig_val': sig_val
				}
				signal['units'] = self.__get_units_from_signals(
					msg_inf.signals,
					sig_name
				)
				msg['signals'].append(signal)
			yield msg

	def signals(self):
		for message in self.messages():
			yield from message['signals']
