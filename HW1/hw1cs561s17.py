import sys
from collections import deque
import heapq

class Neighbor:
	def __init__(self, node, cost):
		self.node = node
		self.cost = int(cost)
	def __repr__(self):
		return "Node:" + self.node + ", " + "Cost:" + self.cost

class PathNode:
	def __init__(self, node, parent, cost):
		self.node = node
		self.parent = parent
		self.cost = int(cost)

def bfs(graph, source, destination, available_fuel):
	source_pathnode = PathNode(source, None, 0)
	queue = deque([source_pathnode])
	visited = {source}
	while queue:
		pathnode = queue.popleft();
		node = pathnode.node
		visited.add(node)
		if node == destination and available_fuel >= pathnode.cost:
			return pathnode
		for neighbor in graph[node]:
			if neighbor.node not in visited and neighbor.node != node:
				child_pathnode = PathNode(neighbor.node, pathnode, pathnode.cost + neighbor.cost)
				queue.append(child_pathnode)
	return None
				

def dfs(graph, source, destination, available_fuel):
	source_pathnode = PathNode(source, None, 0)
	stack = [source_pathnode]
	visited = {source}
	while stack:
		pathnode = stack.pop()
		node = pathnode.node
		visited.add(node)
		if node == destination and available_fuel >= pathnode.cost:
			return pathnode
		for neighbor in graph[node]:
			if neighbor.node not in visited and neighbor.node != node:
				child_pathnode = PathNode(neighbor.node, pathnode, pathnode.cost + neighbor.cost)
				stack.append(child_pathnode)
	return None

def ucs(graph, source, destination, available_fuel):
	source_pathnode = PathNode(source, None, 0)
	priority_queue = []
	heapq.heappush(priority_queue, (source_pathnode.cost, source_pathnode))
	visited = {source}
	while priority_queue:
		pathnode_tuple = heapq.heappop(priority_queue)
		pathnode = pathnode_tuple[1]
		node = pathnode.node
		visited.add(node)
		if node == destination and available_fuel >= pathnode.cost:
			return pathnode
		for neighbor in graph[node]:
			child_pathnode = PathNode(neighbor.node, pathnode, pathnode.cost + neighbor.cost)
			if neighbor.node not in visited and neighbor.node != node:
				heapq.heappush(priority_queue, (child_pathnode.cost, child_pathnode))
			else:
				for index, value in enumerate(priority_queue):
					if value[1].node == child_pathnode.node and value[1].cost > child_pathnode.cost:
						priority_queue[index] = (child_pathnode.cost, child_pathnode)
						heapq.heapify(priority_queue)

	return None

def ascending(list):
	list.sort(key = lambda x: x.node)

def descending(list):
	list.sort(key = lambda x: x.node, reverse = True)

algorithms = {"BFS" : bfs,
	"DFS" : dfs,
	"UCS" : ucs}
sorters = {"BFS": ascending,
	"DFS" : descending,
	"UCS" : ascending}

lines = []
with open(sys.argv[2]) as f:
	lines.extend(f.read().splitlines())
algorithm = lines.pop(0)
available_fuel = int(lines.pop(0))
source = lines.pop(0)
destination = lines.pop(0)
graph = {}
for entry in lines:
	parts = entry.split(": ")
	key = parts[0]
	neighbors = parts[1]
	neighbors = neighbors.split(", ")
	neighbors = [part.split("-") for part in neighbors]
	graph.update({key:[]})
	for neighbor in neighbors:
		graph[key].append(Neighbor(neighbor[0], neighbor[1]))
	sorters[algorithm](graph[key])
pathnode = algorithms[algorithm](graph, source, destination, available_fuel)
output = ""
fo = open("output.txt", "wb")
if pathnode is not None:
	remaining_fuel = available_fuel - pathnode.cost
	while pathnode is not None:
		output = pathnode.node + "-" + output
		pathnode = pathnode.parent
	output = output[:-1] + " " + str(remaining_fuel)
	fo.write(output)
else:
	print "No Path"
fo.write('\n')
fo.close()

