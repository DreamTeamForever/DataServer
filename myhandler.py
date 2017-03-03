import json
from datetime import datetime
from os import listdir
from os.path import isfile, join
import json
from graph import GraphMaker
import strip

gm = GraphMaker()

def getDataChart():
	return(bytes(json.dumps(gm.getData()), 'utf8'))

def getGraphData():
	gm.generateNewData(json.loads(strip.doGET('/PowerSystem/GetShot')))
	return bytes(json.dumps(gm.getResult()), 'utf8')

def saveData(data, name):
	with open("./data/"+name.replace('/', '_'), "wb") as f:
		f.write(data)
	return

def getData(path):
	with open("./data/"+path.replace('/', '_'), "rb") as f:
		return f.read()