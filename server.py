import socket
import multiprocessing
import myhandler

class Server(object):
    def __init__(self, hostname, port):
	import logging
	self.logger = logging.getLogger("server")
	self.hostname = hostname
	self.port = port

    def start(self):
	self.logger.debug("listening")
	self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.socket.bind((self.hostname, self.port))
	self.socket.listen(1)

	while True:
	    conn, address = self.socket.accept()
	    self.logger.debug("Got connection")
	    process = multiprocessing.Process(target = myhandler.handle, args=(conn, address))
	    process.daemon = True
	    process.start()
	    self.logger.debug("Start process %r", process)