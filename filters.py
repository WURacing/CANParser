import canparser
import math

class Rotate2DFilter(canparser.SignalFilter):

	def __init__(self, input_signals, output_signals, theta, greedy=False):

		"""
		Only 2 signals supported for input/output
		"""
		super().__init__(input_signals[:2], output_signals[:2])
		self.theta = theta
		self.greedy = greedy

		"""
		Most recently seen values, and whether they've been modified since the
		last output.
		"""
		self.mrs = [None]*2
		self.modified = [False]*2

	def input(self, signal):

		sig_id = (signal['sender'], signal['msg_name'], signal['sig_name'])

		idx = self.input_signals.index(sig_id)

		self.mrs[idx] = signal
		self.modified[idx] = True

		if all(self.modified) or (self.greedy and None not in self.mrs):
			x,y = self.mrs

			x_outv = x['sig_val'] \
				* math.cos(self.theta) \
				+ y['sig_val'] \
				* math.sin(self.theta)
			y_outv = -x['sig_val'] \
				* math.sin(self.theta) \
				+ y['sig_val'] \
				* math.cos(self.theta)

			x_out = {
				'timestamp': signal['timestamp'],
				'epoch': signal['epoch'],
				'sender': self.output_signals[0][0],
				'msg_name': self.output_signals[0][1],
				'sig_name': self.output_signals[0][2],
				'sig_val': x_outv,
				'units': self.output_signals[0][3]
			}
			y_out = {
				'timestamp': signal['timestamp'],
				'epoch': signal['epoch'],
				'sender': self.output_signals[1][0],
				'msg_name': self.output_signals[1][1],
				'sig_name': self.output_signals[1][2],
				'sig_val': y_outv,
				'units': self.output_signals[1][3]
			}

			if not self.greedy:
				self.modified = [False]*2

			return [x_out, y_out]

		return []

class LinearComboFilter(canparser.SignalFilter):

	def __init__(self, input_signals, output_signal, coeffs, greedy=False):

		if not isinstance(output_signal, list):
			output_signals = [output_signal]
		else:
			output_signals = output_signal[:1]

		super().__init__(input_signals, output_signals)

		self.coeffs = coeffs[:len(input_signals)+1]
		self.greedy = greedy

		"""
		See above class. I'll probably move this functionality over into a super
		class, like GreedyFilter or something.
		"""
		self.mrs = [None]*len(input_signals)
		self.modified = [False]*len(input_signals)

	def input(self, signal):

		sig_id = (signal['sender'], signal['msg_name'], signal['sig_name'])

		idx = self.input_signals.index(sig_id)

		self.mrs[idx] = signal
		self.modified[idx] = True

		if all(self.modified) or (self.greedy and None not in self.mrs):
			out_val = 0
			for sig, coeff in zip(self.mrs, self.coeffs[:-1]):
				out_val += sig['sig_val'] * coeff
			out_val += self.coeffs[-1]

			out_sig = {
				'timestamp': signal['timestamp'],
				'epoch': signal['epoch'],
				'sender': self.output_signals[0][0],
				'msg_name': self.output_signals[0][1],
				'sig_name': self.output_signals[0][2],
				'sig_val': out_val,
				'units': self.output_signals[0][3]
			}

			if not self.greedy:
				self.modified = [False]*len(self.input_signals)

			return [out_sig]

		return []