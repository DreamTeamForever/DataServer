import json
import datetime

def getJsonString():
    res =   [
	  {
	    "object_id": "5899b900bd28fec208de5864",
	    "object_type": "generate",
	    "table_model": "5899b900dee5abbbe63e4104",
	    "name": "ROUGHIES",
	    "description": "Veniam eiusmod dolor esse et. Magna elit aliquip dolore laboris occaecat ut fugiat qui nulla excepteur. Ea minim culpa adipisicing enim enim consectetur enim magna. Exercitation irure ullamco fugiat ea non ullamco enim laboris elit. Laborum elit pariatur nisi nostrud sunt dolore qui eiusmod. Anim ex do dolor eiusmod minim dolore amet mollit irure excepteur dolor.\r\n",
	    "isActive": true,
	    "options": [
	      {
		"id": 0,
		"option_type": "ea",
		"value": 0.5076,
		"status": false
	      },
	      {
		"id": 1,
		"option_type": "aliquip",
		"value": 0.6099,
		"status": true
	      },
	      {
		"id": 2,
		"option_type": "labore",
		"value": 0.8102,
		"status": true
	      }
	    ]
	  },
	  {
	    "object_id": "5899b9007c57c52518b9034a",
	    "object_type": "eat",
	    "table_model": "5899b900707c46374d1869d6",
	    "name": "ULTRASURE",
	    "description": "Veniam officia labore ex aliquip nisi. Tempor officia nostrud irure excepteur consequat fugiat officia labore consectetur esse. Sunt aliqua magna duis aliquip elit laborum mollit.\r\n",
	    "isActive": true,
	    "options": [
	      {
		"id": 0,
		"option_type": "deserunt",
		"value": 0.7316,
		"status": false
	      },
	      {
		"id": 1,
		"option_type": "sint",
		"value": 0.8913,
		"status": false
	      },
	      {
		"id": 2,
		"option_type": "non",
		"value": 0.976,
		"status": false
	      }
	    ]
	  },
	  {
	    "object_id": "5899b900ff40fa0548ea85d2",
	    "object_type": "eat",
	    "table_model": "5899b900b04067f0e409ba03",
	    "name": "MAINELAND",
	    "description": "Eu ullamco dolore nisi tempor eu sit quis nisi ipsum id voluptate. Fugiat deserunt culpa occaecat voluptate officia nisi ut. Fugiat laborum labore adipisicing excepteur.\r\n",
	    "isActive": false,
	    "options": [
	      {
		"id": 0,
		"option_type": "ad",
		"value": 0.0261,
		"status": true
	      },
	      {
		"id": 1,
		"option_type": "duis",
		"value": 0.6172,
		"status": true
	      },
	      {
		"id": 2,
		"option_type": "magna",
		"value": 0.891,
		"status": false
	      }
	    ]
	  },
	  {
	    "object_id": "5899b900de66c93c035e2b92",
	    "object_type": "generate",
	    "table_model": "5899b9005c113e00d579facb",
	    "name": "SCHOOLIO",
	    "description": "Mollit cupidatat sunt duis excepteur commodo ut eu exercitation aute officia id. Voluptate esse sit aliquip qui. Ad aliqua adipisicing laborum aliquip duis sint non qui amet consequat quis commodo. Officia eu proident duis cillum excepteur duis aliqua velit adipisicing. Nostrud duis sit sunt enim sunt sint magna cillum nostrud commodo officia.\r\n",
	    "isActive": true,
	    "options": [
	      {
		"id": 0,
		"option_type": "proident",
		"value": 0.6284,
		"status": false
	      },
	      {
		"id": 1,
		"option_type": "quis",
		"value": 0.7847,
		"status": false
	      },
	      {
		"id": 2,
		"option_type": "enim",
		"value": 0.6826,
		"status": true
	      }
	    ]
	  },
	  {
	    "object_id": "5899b90028824141c0c528a2",
	    "object_type": "generate",
	    "table_model": "5899b90021baa9bfd3740dac",
	    "name": "MARKETOID",
	    "description": "Esse voluptate adipisicing ex labore. Non dolor labore mollit non eiusmod culpa incididunt incididunt elit tempor non esse Lorem. Sint nostrud est laborum sit officia dolor laboris nulla veniam proident ullamco aliqua.\r\n",
	    "isActive": true,
	    "options": [
	      {
		"id": 0,
		"option_type": "labore",
		"value": 0.0468,
		"status": false
	      },
	      {
		"id": 1,
		"option_type": "consectetur",
		"value": 0.6736,
		"status": true
	      },
	      {
		"id": 2,
		"option_type": "cupidatat",
		"value": 0.2417,
		"status": false
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
