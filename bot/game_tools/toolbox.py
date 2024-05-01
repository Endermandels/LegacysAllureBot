from collections import deque

# Game Specific

def all_units_exhausted(units):
	"""
	Receives a dictionary containing both players' units
	"""
	for player in units.keys():
		for unit in units[player]:
			if not unit.exhausted:
				return False
	return True

def can_use_unit(units, p0):
	for unit in units[p0]:
		if not unit.exhausted:
			return True
	return False

def end_of_round(units):
	"""
	Receives a dictionary containing both players' units
	"""
	for player in units.keys():
		for unit in units[player]:
			unit.refresh()

def has_AP(unit):
	return 'AP' in unit.passives

def has_FLY(unit):
	return 'FLY' in unit.passives

def has_PATH(unit):
	return 'PATH' in unit.passives

# Bot Specific

def dfs(board, unit, _hex, depth, all_paths, path=[]):
	"""
	Alters all_paths with legal paths
	"""
	occupying_unit = board[_hex]['occupying']

	if depth == 0:
		if len(path) > 0 and not occupying_unit:
			all_paths.append(path + [_hex])
		return
	
	# Can move through hex
	if not occupying_unit or occupying_unit == unit:
		path.append(_hex)
		if len(path) > 1:
			all_paths.append(path.copy())
	elif has_FLY(unit) or has_PATH(unit):
		path.append(_hex)
	elif has_AP(unit) and unit.p0 == occupying_unit.p0:
		path.append(_hex)
	else:
		return

	for neighbor in board[_hex]['adj spaces']:
		dfs(board, unit, neighbor, depth - 1, all_paths, path)

	path.pop()

def bfs(board, start_hex, dest_hex):
	"""
	Returns a shortest path from start_hex to dest_hex
	Used for calculating the distance from start_hex to dest_hex
	"""
	queue = deque([(start_hex, [start_hex])])

	while queue:
		current_hex, path = queue.popleft()
		occupying_unit = board[current_hex]['occupying']

		if current_hex == dest_hex:
			return path

		for neighbor in board[current_hex]['adj spaces']:
			new_path = path + [neighbor]

			if neighbor == dest_hex:
				return new_path

			queue.append((neighbor, new_path))

	return []

def dist_to_hex(start_hex, dest_hex, board):
	path = bfs(board, start_hex, dest_hex)
	return max(len(path) - 1, 0)

def generate_paths(board, unit):
	"""
	Returns a list of lists.
	Each list contains the unit's start hex and all subsequent hexes from that start hex
	within the unit's movement.
	"""
	all_paths = []
	dfs(board, 
		unit,
		unit.hex, 
		unit.mov, 
		all_paths)

	# print('generated:')
	# for path in all_paths:
	# 	print(path)
	
	return all_paths

def generate_set_destinations(board, unit):
	"""
	Returns a set containing all possible destinations for a unit.
	Excludes the unit's starting hex
	"""
	paths = generate_paths(board, unit)

	result = set()

	for path in paths:
		if path[-1] != unit.hex:
			result.add(path[-1])

	return result

def enemies_adj_hex(board, _hex, p0):
	all_enemies = []
	for h in board[_hex]['adj spaces']:
		occupying_unit = board[h]['occupying']
		if occupying_unit and occupying_unit.p0 == p0:
			all_enemies.append(occupying_unit)
	return all_enemies

def attackable_enemies(board, unit):
	"""
	Returns a list containing all enemies unit can attack
	"""

	# For melee only units
	return enemies_adj_hex(board, unit.hex, not unit.p0)

def num_possible_kills(board, units, p0, attack_unit):
	"""
	NOTE: attack_unit is the function from action.py

	Returns the number of killable enemies next turn and next round.
	Each enemy kill is worth the unit's gold squared.
	Every enemy kill is summed together.
	"""
	next_turn = 0
	next_round = 0

	for unit in units[p0]:
		enemies = attackable_enemies(board, unit)
		for enemy in enemies:
			kill_enemy = attack_unit(unit, enemy, board, pretend=True)
			if kill_enemy:
				next_round += enemy.gold * 3
				if not unit.exhausted:
					next_turn += enemy.gold ** 2

	return next_turn, next_round

def gold_remaining(units, p0):
	"""
	Returns the remaining gold for p0 units and p1 units.
	"""
	allies = 0
	enemies = 0

	for unit in units[p0]:
		allies += unit.gold

	for unit in units[not p0]:
		enemies += unit.gold

	return allies, enemies

def observable_units(board_class, p0):
	"""
	Returns a list of encoded units on each hex.
	units in each hex:
		0 for none
		1 for ally
		2 for exhausted ally
		3 for enemy
		4 for exhausted enemy
	TODO: Tell which unit a unit is (like Swordsman or Crossbowman)
	"""
	results = []
	for _hex in board_class.HEX_LIST:
		unit = board_class.hexes[_hex]['occupying']
		if not unit:
			# No unit
			results.append(0)
		elif unit.p0 == p0:
			# Ally
			if not unit.exhausted:
				results.append(1)
			else:
				results.append(2)
		else:
			# Enemy
			if not unit.exhausted:
				results.append(3)
			else:
				results.append(4)
	return results
