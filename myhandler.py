import json
from datetime import datetime
from os import listdir
from os.path import isfile, join
import json
from graph import GraphMaker
import strip
from shutil import copyfile

gm = GraphMaker()

def resetData():
	gm.data = list()

def getDataChart():
	return(bytes(json.dumps(gm.getData()), 'utf8'))

def getGraphData():
	data = strip.doGET('/PowerSystem/GetShot')
	if data:
		gm.generateNewData(json.loads(data))
	else:
		print('New graph data nod found. Using old graph data.')
	return bytes(json.dumps(gm.getResult()), 'utf8')

def saveData(data, name):
	with open("./data/"+name.replace('/', '_'), "wb") as f:
		f.write(data)
	return

def getData(path):
	with open("./data/"+path.replace('/', '_'), "rb") as f:
		return f.read()

def resetRequest():
	try:
		copyfile('default/_objectCollections', 'data/_objectCollections')
		copyfile('default/_modelCollections', 'data/_modelCollections')
		copyfile('default/_gameSettings', 'data/_gameSettings')
		return True
	except:
		return False