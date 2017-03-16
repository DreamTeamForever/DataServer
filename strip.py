import http.client
import json

server_url = '192.168.1.70:8888'
connection_timeout = 5

def doGET(url):
	try:
		conn = http.client.HTTPConnection(server_url, timeout=connection_timeout)
		conn.request('GET', url)
		response = conn.getresponse()
		data = response.read().decode('utf8') if response.status == 200 else ""
		conn.close()
		return data
	except:
		print('connecting error during doGET')
		return None

def doPOST(url, data):
	try:
		conn = http.client.HTTPConnection(server_url, timeout=connection_timeout)
		conn.request('POST', url, data, {"Content-type": "application/json"})
		response = conn.getresponse()
		conn.close()
		return response
	except:
		print('connecting error during doPOST')
		return None

def startGame():
	buf = {}
	with open('./data/_gameSettings', 'r') as f:
		buf['settings'] = json.loads(f.read())
	with open('./data/_objectCollections', 'r') as f:
		buf['objects'] = json.loads(f.read())
	with open('./data/_modelCollections', 'r') as f:
		buf['models'] = json.loads(f.read())

	res = doPOST('/PowerSystem/StartGame', bytes(json.dumps({"clientmodel": buf}), 'utf8'))
	print(str(res.status), res.read())
	return

def stopGame():
	res = doGET('/PowerSystem/StopGame')
	print(res)
	return


def updateObjects():
	buf = {}
	with open('./data/_objectCollections', 'r') as f:
		buf['objects'] = json.loads(f.read())

	res = doPOST('/PowerSystem/StartGame', bytes(json.dumps({"clientmodel": buf}), 'utf8'))
	print(str(res.status), res.read())
	return
