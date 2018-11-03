import abc
import canparser

"""
The purpose of this class is to provide signals from both
a parser object and an arbitrary list of filters. This is NOT
supposed to be a subclass of CANParser- it depends on whatever
specific parser is passed as argument. I'm open to the idea of
using generics, but this should do for now.
"""
class ParserFilter():

	"""
	We don't actually need a parser, it's also valid for a calling function
	to just pass signals into the filter manually
	"""
	def __init__(self, parser=None, signal_filters):

		self.parser = parser
		self.signal_filters = signal_filters

		"""
		Dictionary from signal identifiers (sender, message_name, sig_name) to
		sets of filter objects with those signals as inputs.
		"""
		self.__sigs_to_filt = {}
		for sig_filt in self.signal_filters:
			for input_signal in sig_filt.input_signals:
				if input_signal not in self.__sigs_to_filt:
					self.__sigs_to_filt[input_signal] = set()
				self.__sigs_to_filt[input_signal].add(sig_filt)

	"""
	Input: one signal object
	Output: A list of any possible output filtered signals from the input
	signal, or an empty list if none
	"""
	def __dispatch_signal_to_filters(self, signal):
		output = []
		sig_id = (signal["sender"], signal())
		for sig_filt in self.__sigs_to_filt[]

	def packets(self):
		if self.parser is not None:
			yield from self.parser.packets()

	def messages(self):
		if self.parser is not None:
			yield from self.parser.messages()

	def signals(self):
		if self.parser is not None:
			yield from self.parser.signals()

	"""
	As of right now filters only apply on the signal level, i.e. there's no
	such thing as filtered messages. This could change in the future.

	Input: a signal or list of signals
	Output: a list containing the inputted signals AND the corresponding
	filtered signals (possibly none)
	"""
	def filter_signal(self, signals):
		

	def filtered_signals(self):
		for signal in self.signals():


class SignalFilter(abc.ABC):

	"""
	A tuple of (sender, msg_name, sig_name) constitutes a unique input signal
	identifier.
	The same combination of fields should be unique for output signals,
	but the argument passed here should be a list of tuples matching
	(sender, msg_name, sig_name, units).
	"""
	def __init__(self, input_signals, output_signals):

		self.input_signals = input_signals
		self.output_signals = output_signals

	"""
	Input: one signal object
	Output: A list of any possible output filtered signals from the input
	signal, or an empty list if none
	"""
	@abc.abstractmethod
	def input(signal):
		pass