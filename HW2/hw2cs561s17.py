import sys


class Assignment:
	def __init__(self, player, color):
		self.player = int(player)
		self.color = color

	def __repr__(self):
		return "'Player:" + str(self.player) + ", " + "Color:" + self.color + "'"


class Action:
	def __init__(self, state, color):
		self.state = state
		self.color = color

	def __repr__(self):
		return "'State:" + self.state + ", " + "Color:" + self.color + "'"


class Maxint:
	def __init__(self):
		self.value = sys.maxint

	def __repr__(self):
		return "inf"

	def __eq__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value == other.value
		return self.value == other

	def __le__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value <= other.value
		return self.value <= other

	def __ge__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value >= other.value
		return self.value >= other

	def __lt__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value < other.value
		return self.value < other

	def __gt__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value > other.value
		return self.value > other


class Minint:
	def __init__(self):
		self.value = - sys.maxint - 1

	def __repr__(self):
		return "-inf"

	def __eq__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value == other.value
		return self.value == other

	def __le__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value <= other.value
		return self.value <= other

	def __ge__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value >= other.value
		return self.value >= other

	def __lt__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value < other.value
		return self.value < other

	def __gt__(self, other):
		if isinstance(other, Maxint) or isinstance(other, Minint):
			return self.value > other.value
		return self.value > other


MAXINT = Maxint()
MININT = Minint()


def str_to_ascii(word):
	return [ord(c) for c in word]


def log(state, color, depth, v, alpha, beta):
	fo.write(", ".join([state, color, str(depth), str(v), str(alpha), str(beta)]))
	fo.write("\n")


def find_actions_for_state(state, current_assignments):
	allowed_colors = set(colors)
	for neighboring_state in state_graph[state]:
		if neighboring_state in current_assignments:
			if current_assignments[neighboring_state].color in allowed_colors:
				allowed_colors.remove(current_assignments[neighboring_state].color)
	return set(Action(state, color) for color in allowed_colors)


def find_actions(current_assignments):
	actions = set()
	visited = set()
	for state in current_assignments.keys():
		for neighbor in state_graph[state]:
			if neighbor not in current_assignments.keys() and neighbor not in visited:
				visited.add(neighbor)
				actions = actions.union(find_actions_for_state(neighbor, current_assignments))
	return sorted(list(actions), key=lambda action: (action.state, action.color))


# The terminal state of the game is that no more nodes could be colored in the map based on rule 2.
# It could be either all nodes in the map have been colored,
# or no possible assignment could be made according to rule 2.
def terminal_test(current_assignments):  # returns true or false
	return not bool(find_actions(current_assignments))


def get_color_point_mapping(player):
	if player == 1:
		return player1_preferences
	return player2_preferences


def set_value_action_mapping(value_action_mapping, value, action):
	if value in value_action_mapping:
		old_action = value_action_mapping[value]
		if (action.state, action.color) > (old_action.state, old_action.color):
			return
	value_action_mapping[value] = action


def utility(current_assignments):
	score = 0
	for assignment in current_assignments.values():
		current_score = get_color_point_mapping(assignment.player)[assignment.color]
		if assignment.player == 1:
			score += current_score
		else:
			score -= current_score
	return score


def result(current_assignments, action, player):
	current_assignments = current_assignments.copy()
	current_assignments[action.state] = Assignment(player, action.color)
	return current_assignments


def max_value(current_assignments, alpha, beta, value_action_mapping, depth, previous_action):  # returns a utility value
	if depth == max_depth or terminal_test(current_assignments):
		v = utility(current_assignments)
		log(previous_action.state, previous_action.color, depth, v, alpha, beta)
		return v
	v = MININT
	for action in find_actions(current_assignments):
		log(previous_action.state, previous_action.color, depth, v, alpha, beta)
		v = max(v, min_value(result(current_assignments, action, 1), alpha, beta, {}, depth + 1, action))
		set_value_action_mapping(value_action_mapping, v, action)
		if v >= beta:
			break
		alpha = max(alpha, v)
	log(previous_action.state, previous_action.color, depth, v, alpha, beta)
	return v


def min_value(current_assignments, alpha, beta, value_action_mapping, depth, previous_action):  # returns a utility value
	if depth == max_depth or terminal_test(current_assignments):
		v = utility(current_assignments)
		log(previous_action.state, previous_action.color, depth, v, alpha, beta)
		return v
	v = MAXINT
	for action in find_actions(current_assignments):
		log(previous_action.state, previous_action.color, depth, v, alpha, beta)
		v = min(v, max_value(result(current_assignments, action, 2), alpha, beta, {}, depth + 1, action))
		set_value_action_mapping(value_action_mapping, v, action)
		if v <= alpha:
			break
		beta = min(beta, v)
	log(previous_action.state, previous_action.color, depth, v, alpha, beta)
	return v


def alpha_beta_search(current_assignments, previous_action):  # return next assignment
	value_action_mapping = {}
	v = max_value(current_assignments, MININT, MAXINT, value_action_mapping, 0, previous_action)
	fo.write(", ".join([value_action_mapping[v].state, value_action_mapping[v].color, str(v)]))


assignments = {}  # state->Assignment
lines = []
with open(sys.argv[2]) as f:
	lines.extend(f.read().splitlines())
colors = set(lines.pop(0).strip().split(", "))
initialAssignments = lines.pop(0).strip().split(", ")
initialAssignment1 = initialAssignments[0].split(": ")
initialAssignment2 = initialAssignments[1].split(": ")
assignments[initialAssignment1[0]] = \
	Assignment(int(initialAssignment1[1].split("-")[1]), initialAssignment1[1].split("-")[0])
assignments[initialAssignment2[0]] = \
	Assignment(int(initialAssignment2[1].split("-")[1]), initialAssignment2[1].split("-")[0])
max_depth = int(lines.pop(0).strip())
# color->score
player1_preferences = dict((item.split(": ")[0], int(item.split(": ")[1])) for item in lines.pop(0).strip().split(", "))
# color->score
player2_preferences = dict((item.split(": ")[0], int(item.split(": ")[1])) for item in lines.pop(0).strip().split(", "))
state_graph = dict((item.strip().split(": ")[0], list(item.strip().split(": ")[1].split(", "))) for item in lines)  # state->Set(cities)
fo = open("output.txt", "wb")
alpha_beta_search(assignments, Action(initialAssignment2[0], initialAssignment2[1].split("-")[0]))
fo.close()
