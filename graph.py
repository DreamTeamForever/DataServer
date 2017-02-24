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
			self.electric_substaion, 
			self.mini_electric_substaion
		]
		self.edges = [
			self.getNewEdge(self.electric_substaion, self.mini_electric_substaion)
		]
		
	def getNewStick(self):
		newStick = {"data": {"id": "stick_{}".format(self.stickCount),"label": "","type": "stick"}}
		self.stickCount += 1
		return newStick

	def getNewEdge(self, source, dest, color = "#6FB1FC", weight = 170):
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


with open('jsonData.txt', 'r') as f:
	data = json.loads(f.read())

gm = GraphMaker()
print('nodes:', gm.nodes)
print('edges:', gm.edges)

"""
ReqiredPower
ReservedGenerators
Generators
AvailPower
Subnets
Substation
"""

# if data['Generators']:
# 	esInputStik = getNewStick()


# print("nodes:", nodes)
# print("edges:", edges)