# Game Specific
CENTER_HEX = 'E4'

def all_units_exhausted(units):
	"""
	Receives a dictionary containing both players' units
	"""
	for player in units.keys():
		for unit in units[player]:
			if not unit.exhausted:
				return False
	return True

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
	Returns whether the full path was followed
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
	elif has_AP(unit) and unit.p1 == occupying_unit.p1:
		path.append(_hex)
	else:
		return

	for neighbor in board[_hex]['adj spaces']:
		dfs(board, unit, neighbor, depth - 1, all_paths, path)

	path.pop()

def generate_paths(board, unit):
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

def enemies_adj_hex(board, _hex, p1):
	all_enemies = []
	for h in board[_hex]['adj spaces']:
		occupying_unit = board[h]['occupying']
		if occupying_unit and occupying_unit.p1 == p1:
			all_enemies.append(occupying_unit)
	return all_enemies

def attackable_hexes(board, unit):
	# For melee only units
	return enemies_adj_hex(board, unit.hex, not unit.p1)
