import sys

MAXINT = sys.maxint
MININT = - sys.maxint - 1


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


def is_neighbor(state1, state2):
	return state2 in state_graph[state1]


def find_actions_for_state(state, current_assignments):
	allowed_colors = set(colors)
	for neighboring_state in state_graph[state]:
		if neighboring_state in current_assignments:
			if current_assignments[neighboring_state].color in allowed_colors:
				allowed_colors.remove(current_assignments[neighboring_state].color)
	if not allowed_colors:
		return None
	return set(Action(state, color) for color in allowed_colors)


def find_actions(current_assignments):
	actions = set()
	for state in state_graph:
		if state not in current_assignments:
			actions = actions.union(find_actions_for_state(state, current_assignments))
	return actions


# The terminal state of the game is that no more nodes could be colored in the map based on rule 2.
# It could be either all nodes in the map have been colored,
# or no possible assignment could be made according to rule 2.
def terminal_test(current_assignments):  # returns true or false
	return not bool(find_actions(current_assignments))


def get_color_point_mapping(player):
	if player == 1:
		return player1_preferences
	return player2_preferences


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
	current_assignments[action.state] = Assignment(player, action.color)
	return current_assignments


def max_value(current_assignments, alpha, beta, value_action_mapping):  # returns a utility value
	if terminal_test(current_assignments):
		return utility(current_assignments)
	v = MININT
	for action in find_actions(current_assignments):
		v = max(v, min_value(result(current_assignments, action, 1), alpha, beta, {}))
		value_action_mapping[v] = action
		if v >= beta:
			return v
		alpha = max(alpha, v)
	return v


def min_value(current_assignments, alpha, beta, value_action_mapping):  # returns a utility value
	if terminal_test(current_assignments):
		return utility(current_assignments)
	v = MAXINT
	for action in find_actions(current_assignments):
		v = min(v, max_value(result(current_assignments, action, 2), alpha, beta, {}))
		value_action_mapping[v] = action
		if v <= alpha:
			return v
		beta = min(beta, v)
	return v


def alpha_beta_search(current_assignments):  # return next assignment
	value_action_mapping = {}
	v = max_value(current_assignments, MININT, MAXINT, value_action_mapping)
	return value_action_mapping[v]


assignments = {}  # state->Assignment
lines = []
with open(sys.argv[2]) as f:
	lines.extend(f.read().splitlines())
colors = set(lines.pop(0).split(", "))
initialAssignments = lines.pop(0).split(", ")
initialAssignment1 = initialAssignments[0].split(": ")
initialAssignment2 = initialAssignments[1].split(": ")
assignments[initialAssignment1[0]] = \
	Assignment(int(initialAssignment1[1].split("-")[1]), initialAssignment1[1].split("-")[0])
assignments[initialAssignment2[0]] = \
	Assignment(int(initialAssignment2[1].split("-")[1]), initialAssignment2[1].split("-")[0])
max_depth = int(lines.pop(0))
# color->score
player1_preferences = dict((item.split(": ")[0], int(item.split(": ")[1])) for item in lines.pop(0).split(", "))
# color->score
player2_preferences = dict((item.split(": ")[0], int(item.split(": ")[1])) for item in lines.pop(0).split(", "))
state_graph = dict((item.split(": ")[0], set(item.split(": ")[1].split(", "))) for item in lines)  # state->Set(cities)
print alpha_beta_search(assignments)
