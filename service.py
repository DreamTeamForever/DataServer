#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import myhandler
import strip

antiPost = ['/']

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
	def setup(self):
		BaseHTTPRequestHandler.setup(self)
		self.request.settimeout(10)

	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.send_header('Access-Control-Allow-Origin','*')

		if self.path == '/':
			message = bytes(myhandler.getJsonString(), "utf8")
		elif self.path == '/testGraphData':
			message =  myhandler.getGraphData()
		elif self.path == '/dataChart':
			message =  myhandler.getDataChart()
		elif self.path == '/gameTime':
			message = myhandler.getGameTime()
		elif self.path == '/economicData':
			message = myhandler.getEconomicData()
		else:
			try:
				message =  myhandler.getData(self.path)
			except:
				message = bytes("", "utf8")
				self.send_response(404)
		
		self.end_headers()
		self.wfile.write(message)
		return

	def do_POST(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.send_header('Access-Control-Allow-Origin','*')
		if not self.path in antiPost :
			if self.path == '/startGame':
				if not strip.startGame():
					self.send_response(500)
			elif self.path == '/stopGame':
				myhandler.resetData()
				if not strip.stopGame():
					self.send_response(500)
					
			elif self.path == '/resetDefault':
				print('restart')
				if not myhandler.resetRequest():
					self.send_response(500)
			else:
				content_len = int(self.headers['Content-Length'])
				data = self.rfile.read(content_len)
				myhandler.saveData(data, self.path)
				if strip.isStarted() and self.path == '/objectCollections':
					strip.updateObjects()
		else:
			self.send_response(404)
		self.end_headers()	
		return;

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""thet's all =)"""

if __name__ == '__main__':
	print("starting server...")
	server_address = ('', 9099)
	httpd =  ThreadedHTTPServer(server_address, MyHTTPRequestHandler)
	print("running server... use <Ctrl-C> to stop")
	httpd.serve_forever()
