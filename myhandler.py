import json
import datetime

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
    return json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))+'\n'

def saveData(data, address):
    fName = "{}_{}".format(address[0], datetime.datetime.now().strftime("%H:%M:%S_%d.%m.%Y"))
    with open("./data/"+fName, "w") as f:
	f.write(data)
    return fName

def handle(connection, address):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    try:
	logger.debug("Connected %r at %r", connection, address)
	connection.sendall(getJsonString())
	while True:
	    data = connection.recv(1024)
	    if data:
		logger.debug("Have a new data from the Client!")
		logger.debug("Data is saved in '%r' file", saveData(data, address))
		logger.debug("Sending back data")
		connection.sendall(data)
	    else:
		logger.debug("No data from the Client")
		break
    except:
	logger.exception("Problem handling request")
    finally:
	logger.debug("Closing socket")
	connection.close()
	return