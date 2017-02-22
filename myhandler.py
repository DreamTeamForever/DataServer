import json
from datetime import datetime
from os import listdir
from os.path import isfile, join

def getJsonString():
    res =   [
		{"object_id": 1,
		 "object_type": "type1",
		 "table_model": "table1",
		 "options": [
				{"option_type": "option1",
				 "value": 0.01,
				 "status": "stat1"
				},
				{"option_type": "option2",
				 "value": 0.02,
				 "status": "stat2"
				}
			    ]
		},
		{"object_id": 2,
		 "object_type": "type2",
		 "table_model": "model2",
		 "options": [
				{"option_type": "option3",
				 "value": 0.03,
				 "status": "stat3"
				},
				{"option_type": "option4",
				 "value": 0.04,
				 "status": "stat4"
				}
			    ]
		}
	    ]
    return json.dumps(res)

def saveData(data, name):
	with open("./data/"+name.replace('/', '_'), "wb") as f:
		f.write(data)
	return

def getData(path):
	with open("./data/"+path.replace('/', '_'), "rb") as f:
		return f.read()

def getList():
	result = "<http><body>"
	result += "".join(["<p><a href=\"http://82.117.171.124:9099{0}\">{0}</a></p>".format(i.replace('_', '/')) for i in listdir("./data/") if isfile(join("./data/", i))])
	result += "</body></http>"
	return result
