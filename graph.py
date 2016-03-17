import networkx as nx

class Graph:
	g = None
	sections = None

	def __init__(self, places, sections):
		self.g = nx.Graph()
		self.sections = sections
		for i in places:
			self.g.add_node(i['place'], type=i['type'], entrance=i['entrance'])
			if (self.g.node[i['place']]['type'].upper() == 'PARKING'):
				self.g.node[i['place']]['section'] = self.get_section_info(self.find_section(i['place']))
			for j in i['neighbors']:
				self.g.add_edge(i['place'], j, weight=1)

	def get_closest_parking_section(self, dstNodeId, tolerance=5):
		paths = []
		for i in self.find_entrances():
			path = nx.dijkstra_path(self.g, i, dstNodeId)
			while (self.g.node[path[-1]]['type'].upper() != 'PARKING'):
				path.pop()
			paths.append(path)

		for i in xrange(0, len(paths)):
			paths[i] = paths[i][-1]

		if len(paths) == 1:
			paths = paths[0]
		return paths

	def find_entrances(self):
		entrances = []
		for i in self.g.nodes(data=True):
			if 'entrance' in i[1] and i[1]['entrance']:
				entrances.append(i[0])
		return entrances
	
	def get_section_info(self, section):
		data = {}
		if section != None:
			data['free_spaces'] = section['capacity']
			data['max_spaces'] = section['max']
		return data

	def find_section(self, name):
		for i in self.sections:
			if name == i['section']:
				return i
		return None

	def text(self):
		text = 'Nodes: \n'
		for i in self.g.nodes(data=True):
			text += str(i) + '\n'
		text += '\nEdges:\n'
		for i in self.g.edges(data=True):
			text+= str(i) + '\n'
		text+= '\n'
		return text

	def html_text(self):
		return self.text().replace('\n','<br>')

	def display(self):
		print self.text()

#if __name__ == '__main__':
#	places = json.loads('[{"neighbors": ["P_Entrance"], "type": "landmark", "entrance": true, "_id": {"$oid": "56ea122dffe947199ac68972"}, "place": "Entrance"}, {"neighbors": ["P_Residencias", "P_Entrance"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68973"}, "place": "Residencias"}, {"neighbors": ["Centro de Congresos", "P_Entrance", "P_Centro de Congresos", "Aulas I y II"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68974"}, "place": "Cafeteria y Oficinas"}, {"neighbors": ["Cafeteria y Oficinas", "P_Centro de Congresos", "P_Visitantes", "P_Medicina"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68975"}, "place": "Centro de Congresos"}, {"neighbors": ["Cultural y Alberca", "Aulas I y II", "P_Medicina"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68976"}, "place": "MedArq A3 A4"}, {"neighbors": ["MedArq A3 A4", "Cafeteria y Oficinas", "Biblioteca y C_Plaza", "P_Oficinas"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68977"}, "place": "Aulas I y II"}, {"neighbors": ["Aulas I y II", "P_Biblioteca", "C_Medios y Gym", "Cultural y Alberca"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68978"}, "place": "Biblioteca y C_Plaza"}, {"neighbors": ["P_Centro de Medios", "Canchas", "Biblioteca y C_Plaza"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68979"}, "place": "C_Medios y Gym"}, {"neighbors": ["P_Biblioteca"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac6897a"}, "place": "Prepa"}, {"neighbors": ["MedArq A3 A4", "Canchas", "Biblioteca y C_Plaza"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac6897b"}, "place": "Cultural y Alberca"}, {"neighbors": ["Cultural y Alberca", "C_Medios y Gym"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac6897c"}, "place": "Canchas"}, {"neighbors": ["P_Ingenieria"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac6897d"}, "place": "Ingenieria y CDA"}, {"neighbors": ["P_Civil"], "type": "landmark", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac6897e"}, "place": "Civil"}, {"neighbors": ["MedArq A3 A4", "Centro de Congresos"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac6897f"}, "place": "P_Medicina"}, {"neighbors": ["Centro de Congresos"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68980"}, "place": "P_Visitantes"}, {"neighbors": ["Centro de Congresos", "Cafeteria y Oficinas", "P_Entrance"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68981"}, "place": "P_Centro de Congresos"}, {"neighbors": ["Entrance", "Cafeteria y Oficinas", "Residencias", "P_Oficinas", "P_Residencias", "P_Centro de Congresos"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68982"}, "place": "P_Entrance"}, {"neighbors": ["P_Entrance", "Residencias"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68983"}, "place": "P_Residencias"}, {"neighbors": ["P_Entrance", "Aulas I y II", "P_Biblioteca"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68984"}, "place": "P_Oficinas"}, {"neighbors": ["P_Centro de Medios", "Prepa", "Biblioteca y C_Plaza", "P_Oficinas"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68985"}, "place": "P_Biblioteca"}, {"neighbors": ["P_Ingenieria", "C_Medios y Gym", "P_Biblioteca", "P_Civil"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68986"}, "place": "P_Centro de Medios"}, {"neighbors": ["Ingenieria y CDA", "P_Civil", "P_Centro de Medios"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68987"}, "place": "P_Ingenieria"}, {"neighbors": ["Civil", "P_Centro de Medios", "P_Ingenieria"], "type": "parking", "entrance": false, "_id": {"$oid": "56ea122dffe947199ac68988"}, "place": "P_Civil"}]')
#	sections = json.loads('[{"max": 291, "section": "P_Civil", "_id": {"$oid": "56e9c520e3629877b0fd4e92"}, "capacity": 150}, {"max": 446, "section": "P_Ingenieria", "_id": {"$oid": "56e9c52de3629877b0fd4e93"}, "capacity": 200}, {"max": 412, "section": "P_Medicina", "_id": {"$oid": "56e9c53ce3629877b0fd4e94"}, "capacity": 200}, {"max": 237, "section": "P_Visitantes", "_id": {"$oid": "56e9c542e3629877b0fd4e95"}, "capacity": 150}, {"max": 288, "section": "P_Centro de Congresos", "_id": {"$oid": "56e9c5d8e3629877b0fd4e96"}, "capacity": 206}, {"max": 230, "section": "P_Residencias", "_id": {"$oid": "56e9c5eee3629877b0fd4e97"}, "capacity": 210}, {"max": 270, "section": "P_Entrance", "_id": {"$oid": "56e9c623e3629877b0fd4e98"}, "capacity": 100}, {"max": 341, "section": "P_Oficinas", "_id": {"$oid": "56e9c63de3629877b0fd4e99"}, "capacity": 120}, {"max": 269, "section": "P_Biblioteca", "_id": {"$oid": "56e9c6b4e3629877b0fd4e9a"}, "capacity": 150}, {"max": 230, "section": "P_Centro de Medios", "_id": {"$oid": "56e9c6d2e3629877b0fd4e9b"}, "capacity": 150}]')
#	g = Graph(places, sections)
#	g.display()
#	print g.get_closest_parking_section('Ingenieria y CDA')