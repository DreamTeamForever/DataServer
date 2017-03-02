#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import myhandler

antiPost = ['/']

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
	isStart = False

	def setup(self):
		BaseHTTPRequestHandler.setup(self)
		self.request.settimeout(10)

	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.send_header('Access-Control-Allow-Origin','*')

		if self.path == '/':
			message = bytes(myhandler.getJsonString(), "utf8")
		# elif self.path == '/testGraphData':
		# 	message =  myhandler.getGraphData()
		elif self.path == '/dataChart':
			message =  myhandler.getDataChart()
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
				self.isStart = True
				print('start game')
				#strip.startGame()
			elif self.path == '/stopGame':
				self.isStart = False
				print('stop game')
				#strip.stopGame()
			else:
				content_len = int(self.headers['Content-Length'])
				myhandler.saveData(self.rfile.read(content_len), self.path)
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