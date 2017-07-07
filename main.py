import tornado.ioloop
import tornado.websocket
import tornado.web

import serial

socket_users = []
results = multiprocessing.Queue()

class MirrorSocket(tornado.websocket.WebSocketHandler):
	def open(self):
		socket_users.append(self)

	def on_message(self, message):
		pass

	def on_close(self):
		socket_users.remove(self)


class RootPage(tornado.web.RequestHandler):
	def get(self):
		self.write("This is a websocket server that reflects the serial output of the QNet DAQ card.  ")

def copy_queue():
	while not results.empty():
		m = results.get()
		for c in socket_users:
			c.write_message(m)

def make_app():
	return tornado.web.Application([
		(r"/", RootPage),
		(r"/socket", MirrorSocket)
	])


if __name__ == "__main__":
	rd = read_daq.DaqReader(results)
	rd.start()
	app = make_app()
	app.listen(8888)
	scheduler = tornado.ioloop.PeriodicCallback(
		copy_queue, 100, io_loop = mainLoop
	)
	scheduler.start()
	tornado.ioloop.IOLoop.current().start()
