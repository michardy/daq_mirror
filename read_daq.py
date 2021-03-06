#Based on a very useful tutorial: 
#http://fabacademy.org/archives/2015/doc/WebSocketConsole.html

import serial
import multiprocessing


class DaqReader(multiprocessing.Process):
	def __init__(self, results, port="/dev/ttyUSB0"):
		super().__init__()
		self.port = serial.Serial(port, baudrate=115200, timeout=3.0)
		self.results = results #multiprocessing.Queue object
		self.daemon = True

	def read_line(self):
		self.results.put(
			self.port.readline()
		)

	def close(self):
		self.port.close()
	
	def run(self):
		self.port.reset_input_buffer()
		while True:
			if self.port.inWaiting() > 74:
				self.read_line()
