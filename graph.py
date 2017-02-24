import json
import strip


class GraphMaker:
	def __init__(self):
		self.stickCount = 0
		self.electric_substaion = {
			'data':{
				"id": "electric_substaion_0",
				"label": "\u042d\u043b\u0435\u043a\u0442\u0440\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0441\u0442\u0430\u043d\u0446\u0438\u044f",
				"type": "electric_substaion"
			}
		}
		self.mini_electric_substaion = {
		    "data": {
		        "id": "mini_electric_substaion_0",
		        "label": "\u042d\u043b\u0435\u043a\u0442\u0440\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u043f\u043e\u0434\u0441\u0442\u0430\u043d\u0446\u0438\u044f",
		        "type": "mini_electric_substaion"
		    }
		}
		self.nodes = [
			self.electric_substaion
		]
		self.edges = []
		
	def getNewStick(self):
		newStick = {"data": {"id": "stick_{}".format(self.stickCount),"label": "","type": "stick"}}
		self.stickCount += 1
		return newStick

	def getNewEdge(self, source, dest, color = "#6FB1FC", weight = 10):
		edge = {
			'data':{
				'color': color,
				'id': '{}_{}'.format(source['data']['id'], dest['data']['id']),
				'source': source['data']['id'],
				'target': dest['data']['id'],
				"weight": weight
			}
		}
		return edge

	def getResult(self):
		return {'nodes': self.nodes, 'edges': self.edges}

	def getNewNode(self, data):
		buf = {}
		buf['id'] = data['Ident']
		if 'Wind' in data['Ident']:
			buf['type'] = "wind"
			buf['label'] = "\u0412\u0435\u0442\u0440\u043e\u0433\u0435\u043d\u0435\u0440\u0430\u0442\u043e\u0440 " + data['Ident'].split('_')[-1]
		elif 'Solar' in data['Ident']:
			buf['type'] = 'sun'
			buf['label'] = "\u0421\u043e\u043b\u043d\u0435\u0447\u043d\u0430\u044f \u0431\u0430\u0442\u0430\u0440\u0435\u044f " + data['Ident'].split('_')[-1]
		elif 'Diesel' in data['Ident']:
			buf['type'] = 'disel'
			buf['label'] = "\u0414\u0438\u0437\u0435\u043b\u044c \u0433\u0435\u043d\u0435\u0440\u0430\u0442\u043e\u0440 " + data['Ident'].split('_')[-1]
		elif 'Accumulator' in data['Ident']:
			buf['type'] = 'accumulate'
			buf['label'] = "\u042d\u043b\u0435\u043a\u0442\u0440\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u043a\u043a\u0443\u043c\u0443\u043b\u044f\u0442\u043e\u0440_" + data['Ident'].split('_')[-1]
		elif 'Hospital' in data['Ident']:
			buf['type'] = 'hospital'
			buf['label'] = "\u0413\u043e\u0441\u043f\u0438\u0442\u0430\u043b\u044c " + data['Ident'].split('_')[-1]	
		elif 'ResidentialCommunity' in data['Ident']:
			buf['type'] = 'district'
			buf['label'] = "\u041c\u0438\u043a\u0440\u043e\u0440\u0430\u0439\u043e\u043d " + data['Ident'].split('_')[-1]	
		elif 'Factory' in data['Ident']:
			buf['type'] = 'factory'
			buf['label'] = "\u0424\u0430\u0431\u0440\u0438\u043a\u0430 " + data['Ident'].split('_')[-1]	
		else:
			buf['type'] = 'unknown'
			buf['label'] = 'хз чо это'
		return {'data':buf}

	def generateNewData(self, data):
		if 'Generators' in data:
			esStick = self.getNewStick()
			self.nodes.append(esStick)
			self.edges.append(self.getNewEdge(self.electric_substaion, esStick))
			for i in data['Generators']:
				g = self.getNewNode(i) 
				self.nodes.append(g)
				self.edges.append(self.getNewEdge(esStick, g, "#74E883" if i['IsOn'] else "#E8747C"))

		if 'ReservedGenerators' in data:
			esStick = self.getNewStick()
			self.nodes.append(esStick)
			self.edges.append(self.getNewEdge(self.electric_substaion, esStick))
			for i in data['ReservedGenerators']:
				g = self.getNewNode(i) 
				self.nodes.append(g)
				self.edges.append(self.getNewEdge(esStick, g, "#74E883" if i['IsOn'] else "#E8747C"))

		if 'Subnets' in data:
			for i in data['Subnets']:
				esStick = self.getNewStick()
				self.nodes.append(esStick)
				self.edges.append(self.getNewEdge(self.electric_substaion, esStick))
				for j in i['Items']:
					g = self.getNewNode(j) 
					self.nodes.append(g)
					self.edges.append(self.getNewEdge(esStick, g, "#74E883" if i['IsOn'] else "#E8747C"))

		if 'Substation' in data:
			self.nodes.append(self.mini_electric_substaion)
			self.edges.append(self.getNewEdge(self.electric_substaion, self.mini_electric_substaion))
			if 'Subnets' in data['Substation']:
				for i in data['Substation']['Subnets']:
					esStick = self.getNewStick()
					self.nodes.append(esStick)
					self.edges.append(self.getNewEdge(self.mini_electric_substaion, esStick))
					for j in i['Items']:
						g = self.getNewNode(j) 
						self.nodes.append(g)
						self.edges.append(self.getNewEdge(esStick, g, "#74E883" if i['IsOn'] else "#E8747C"))

		return

# gm = GraphMaker()
# with open('jsonData.txt', 'r') as f:
# 	gm.generateNewData(json.loads(f.read()))
# testJson = bytes(json.dumps(gm.getResult()), 'utf8')
# strip.doPOST('/testGraphData', testJson)