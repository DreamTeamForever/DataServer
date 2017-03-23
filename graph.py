import json
from time import gmtime, strftime


class GraphMaker:
	def __init__(self):
		self.stickCount = 0
		self.gameTime = 0
		self.step = -1
		self.maxDataSize = 100
		self.partsProportions = int(self.maxDataSize * 2/3)
		self.nextRemoved = 1
		self.data = list()
		self.nodes = dict()
		self.edges = list()
		
	def getNewStick(self, node):
		i = "stick_{}".format(self.stickCount)
		newStick = {"data": {"id": i,"label": "","type": "stick","color_node": "#1ab394"}}
		self.stickCount += 1
		self.nodes[i] = newStick
		self.createNewEdge(node, newStick)
		return newStick

	def createNewEdge(self, source, dest, color = "#6FB1FC", weight = 10):
		edge = {
			'data':{
				'color': color,
				'id': '{}_{}'.format(source['data']['id'], dest['data']['id']),
				'source': source['data']['id'],
				'target': dest['data']['id'],
				"weight": weight
			}
		}
		self.edges.append(edge)
		return

	def getResult(self):
		return {'nodes': [self.nodes[i] for i in self.nodes], 'edges': self.edges}

	def getEdgeColor(self, i):
		return "#74E883" if i['IsOn'] else "#E8747C"

	def getNodeColor(self, i):
		if 'AvailPower' in i and 'ReqiredPower' in i:
			return "#74E883" if i['AvailPower'] >= i['ReqiredPower'] else "#E8747C"
		return "#1ab394"

	def getData(self):
		return self.data

	def getNode(self, nodeId):
		if nodeId in self.nodes:
			return self.nodes[nodeId]
		else:
			return None

	def createNewNode(self, data):
		if data['Ident'] in self.nodes:
			return self.nodes[data['Ident']]
		buf = dict()
		buf['id'] = data['Ident']
		buf['color_node'] = 'red' #self.getNodeColor(data) 
		if 'MS' in data['Ident']:
			buf['type'] = "electric_substaion"
			buf['label'] = "Подстанция"
		elif 'SS' in data['Ident']:
			buf['type'] = "mini_electric_substaion"
			buf['label'] = "Миниподстанция"
		elif 'GW' in data['Ident']:
			buf['type'] = "wind"
			buf['label'] = "\u0412\u0435\u0442\u0440\u043e\u0433\u0435\u043d\u0435\u0440\u0430\u0442\u043e\u0440 #" + data['Ident'].split('_')[-1]
		elif 'GS' in data['Ident']:
			buf['type'] = 'sun'
			buf['label'] = "\u0421\u043e\u043b\u043d\u0435\u0447\u043d\u0430\u044f \u0431\u0430\u0442\u0430\u0440\u0435\u044f #" + data['Ident'].split('_')[-1]
		elif 'GRD' in data['Ident']:
			buf['type'] = 'disel'
			buf['label'] = "\u0414\u0438\u0437\u0435\u043b\u044c \u0433\u0435\u043d\u0435\u0440\u0430\u0442\u043e\u0440 #" + data['Ident'].split('_')[-1]
		elif 'GRA' in data['Ident']:
			buf['type'] = 'accumulate'
			buf['label'] = "\u042d\u043b\u0435\u043a\u0442\u0440\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0430\u043a\u043a\u0443\u043c\u0443\u043b\u044f\u0442\u043e\u0440 #" + data['Ident'].split('_')[-1]
		elif 'CH' in data['Ident']:
			buf['type'] = 'hospital'
			buf['label'] = "Больница #" + data['Ident'].split('_')[-1]	
		elif 'CU' in data['Ident']:
			buf['type'] = 'district'
			buf['label'] = "\u041c\u0438\u043a\u0440\u043e\u0440\u0430\u0439\u043e\u043d #" + data['Ident'].split('_')[-1]	
		elif 'CF' in data['Ident']:
			buf['type'] = 'factory'
			buf['label'] = "\u0424\u0430\u0431\u0440\u0438\u043a\u0430 #" + data['Ident'].split('_')[-1]
		elif 'SN' in data['Ident']:
			buf['type'] = 'stick'
			buf['color_node'] = '#1ab394'
			buf['label'] = ""	
		else:
			buf['type'] = 'unknown'
			buf['label'] = 'неопределено'
		node = {'data': buf}
		self.nodes[buf['id']] = node
		return node

	def insertData(self, obj):
		d = {
		        "step": strftime("%d:%H:%M", gmtime(self.step*1200)),
		        "input": obj["AvailPower"] if "AvailPower" in obj else -1,
		        "output": obj["ReqiredPower"] if "ReqiredPower" in obj else -1,
		        "average_load": str(obj["Overload"] if "Overload" in obj else -1) 
      		}

		for i in self.data:
			if i['object_id'] == obj['Ident']:
				if len(i['object_data']) >= self.maxDataSize:
					del i['object_data'][self.nextRemoved]
					self.nextRemoved = (self.nextRemoved % self.partsProportions) + 1
				i['object_data'].append(d)
				return
		self.data.append({'object_id': obj['Ident'], 'object_data':[d]})
		return

	def processingGenerators(self, target, data):
		stick_MS_Generators = self.getNewStick(target)
		for i in data:
			if i == None:
				self.getNewStick(stick_MS_Generators)
			else:
				newGenerator = self.createNewNode(i)
				self.insertData(i)
				self.createNewEdge(stick_MS_Generators, newGenerator, self.getEdgeColor(i))

	def processingSubnets(self, target, data):
		for subnet in data:
			if subnet == None:
				continue
			else:
				snNode = self.createNewNode(subnet)
				self.insertData(subnet)
				self.createNewEdge(target, snNode, self.getEdgeColor(subnet))
				#processing information about subnet items
				for i in subnet['Items']:
					iNode = self.createNewNode(i)
					#saving info about item links
					self.items.append(i)

	def processinSubstation(self, data):
		try:
			nodeMS = self.createNewNode(data)
			self.insertData(data)
		except Exception as e:
			print("Crating electric substation failed!")
			print(str(e))
			return None

		#processing info about generaters
		if 'Generators' in data:
			self.processingGenerators(nodeMS, data['Generators'])

		#processing info about reserved generaters
		if 'ReservedGenerators' in data:
			self.processingGenerators(nodeMS, data['ReservedGenerators'])

		#processing information about electric substation subnets
		if 'Subnets' in data:
			self.processingSubnets(nodeMS, data['Subnets'])
		return nodeMS

	def getGameTime(self):
		return strftime("%d:%H:%M", gmtime(self.step*1200))

	def getEconomicData(self):
		#{'object_data': [{'input': 401.4, 'average_load': '57', 'output': 700, 'step': 1}], 'object_id': 'MS_001'
		return [{'object_id': i['object_id'], 'object_data': [{'incom': 2.45*abs(j['input'] - j['output']), 'step': j['step']} for j in i['object_data']]} for i in self.getData()] 

	def generateNewData(self, data):
		try:
			time = data['ModelTime'] if 'ModelTime' in data else (self.step + 1)
			if time == self.step:
				return
			self.nodes = dict()
			self.edges = list()
			self.items = list() #for saving inforamtion about items links
			self.step = time
			self.stickCount = 0
			#insert info about substation
			nodeMS = self.processinSubstation(data)
			if not nodeMS:
				return

			#processing information about mini electric substation
			if 'Substation' in data:
				nodeSS = self.processinSubstation(data['Substation'])
				if nodeSS:
					self.createNewEdge(nodeMS, nodeSS, self.getEdgeColor(data['Substation']))
				else:
					print('Mini electric station: getting information failed')


			#processing information about consumer items links
			for item in self.items:
				self.insertData(item)
				iNode = self.getNode(item['Ident'])
				if not iNode:
					print('Item node not found')
					continue
				for link in item['SubnetLinks']:
					if link == None:
						continue
					snNode = self.getNode(link['SubnetLink'])
					if not snNode:
						continue
					self.createNewEdge(iNode, snNode, self.getEdgeColor(link))

		except Exception as e:
			print('Error during generateNewData')
			print(str(e))
		return
