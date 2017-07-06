import tornado.ioloop
import tornado.websocket
import tornado.web

import serial

class MirrorSocket(tornado.websocket.WebSocketHandler):
	def open(self):
		print("WebSocket opened")

    def on_message(self, message):
		pass

	def on_close(self):
		print("WebSocket closed")


class RootPage(tornado.web.RequestHandler):
	def get(self):
		self.write("This is a websocket server that reflects the serial output of the QNet DAQ card.  ")

def make_app():
	return tornado.web.Application([
		(r"/", RootPage),
		(r"/socket", MirrorSocket)
	])

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
