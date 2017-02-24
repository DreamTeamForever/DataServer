import http.client

server_url = 'ascae.ru:9099'

def doGET(url):
	conn = http.client.HTTPConnection(server_url)
	conn.request('GET', url)
	response = conn.getresponse()
	conn.close()
	return response.read().decode('utf8') if response.status == 200 else ""

def doPOST(url, data):
	conn = http.client.HTTPConnection(server_url)
	conn.request('POST', url, data)
	response = conn.getresponse()
	conn.close()
	return response.status