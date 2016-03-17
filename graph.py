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
				self.g.node[i['place']]['section'] = self.find_section(i['place'])
			for j in i['neighbors']:
				self.g.add_edge(i['place'], j[0], weight=j[1])

	def get_closest_parking_section(self, dstNodeId, tolerance=5):
		paths = []
		for i in self.find_entrances():
			path = nx.dijkstra_path(self.g, i, dstNodeId)
			while (self.g.node[path[-1]]['type'].upper() != 'PARKING'):
				path.pop()
			paths.append(path)

		destinations = []
		for i in xrange(0, len(paths)):
			destinations.append(paths[i][-1])

		for i in xrange(0,len(destinations)):
			section = self.g.node[destinations[i]]['section']
			free = float(section['capacity']) / section['max'] * 100
			prevFound = [destinations[i]]
			while (free < tolerance):
				destinations[i] = self.find_neighbor_with_parking_spots(destinations[i], exclude=prevFound)
				prevFound.append(destinations[i])
				section = self.g.node[destinations[i]]['section']
				free = float(section['capacity']) / section['max'] * 100

		if len(destinations) == 1:
			destinations = destinations[0]

		return destinations

	def find_neighbor_with_parking_spots(self, nodeId, exclude=[]):
		for nid in self.g.neighbors(nodeId):
			if self.g.node[nid]['type'].upper() == 'PARKING' and nid not in exclude:
				return nid
		return None

	def find_entrances(self):
		entrances = []
		for i in self.g.nodes(data=True):
			if 'entrance' in i[1] and i[1]['entrance']:
				entrances.append(i[0])
		return entrances

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

	def to_dict(self):
		return {'nodes': self.g.nodes(data=True), 'edges': self.g.edges(data=True)}

	def display(self):
		print self.text()