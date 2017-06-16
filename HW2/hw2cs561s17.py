import sys
from sets import Set

class Assignment:
	def __init__(self, player, depth, color):
		self.player = int(player)
		self.depth = int(depth)
		self.color = color
	def __repr__(self):
		return "'Player:" + str(self.player) + ", " + "Depth:" + str(self.depth) + ", " + "Color:" + self.color + "'"

assignments = {} # city->Assignment
player1_preferences = {} # color->score
player2_preferences = {} # color->score
city_graph = {} #city->Set(cities)
lines = []
with open(sys.argv[2]) as f:
	lines.extend(f.read().splitlines())
colors = lines.pop(0).split(", ")
initialAssignments = lines.pop(0).split(", ")
initialAssignment1 = initialAssignments[0].split(": ")
initialAssignment2 = initialAssignments[1].split(": ")
assignments[initialAssignment1[0]] = Assignment(1, 0, initialAssignment1[1])
assignments[initialAssignment2[0]] = Assignment(2, 1, initialAssignment2[1])
max_depth = int(lines.pop(0))
player1_preferences = dict(item.split(": ") for item in lines.pop(0).split(", "))
player2_preferences = dict(item.split(": ") for item in lines.pop(0).split(", "))
city_graph = dict((item.split(": ")[0], Set(item.split(": ")[1].split(", "))) for item in lines)
