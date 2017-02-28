import http.client
import json

server_url = '10.0.0.4:8888'
def doGET(url):
	conn = http.client.HTTPConnection(server_url)
	conn.request('GET', url)
	response = conn.getresponse()
	data = response.read().decode('utf8') if response.status == 200 else ""
	conn.close()
	return data

def doPOST(url, data):
	print(data)
	conn = http.client.HTTPConnection(server_url)
	conn.request('POST', url, data, {"Content-type": "application/json"})
	response = conn.getresponse()
	print("{} {} {}".format(response.status, response.reason, response.read().decode('utf8')))
	conn.close()
	return response


def startGame():
	buf = {}
	with open('./data/_gameSettings', 'r') as f:
		buf['settings'] = json.loads(f.read())
	with open('./data/_objectCollections', 'r') as f:
		buf['objects'] = json.loads(f.read())
	with open('./data/_modelCollections', 'r') as f:
		buf['models'] = json.loads(f.read())

	request_data = bytes(json.dumps(buf), 'utf8')
	res = doPOST('/PowerSystem/StartGame', request_data)
	print(str(res.status), res.read())

	return

def stopGame():
	doGET('/PowerSystem/StopGame')
	return