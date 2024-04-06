"""
Handles each action:
	Attack
	Move
	Pass
"""

DEBUG = True

def pass_unit(unit):
	unit.exhaust()

	if DEBUG:
		print('Passed ' + unit.name + ' on ' + unit.hex)

def move_unit(unit, _hex, board):
	prev_hex = unit.hex

	board[unit.hex]['occupying'] = None
	unit.hex = _hex
	board[unit.hex]['occupying'] = unit
	unit.exhaust()

	if DEBUG:
		print('Moved ' + unit.name + ' from ' + prev_hex + ' to ' + unit.hex)

def attack_unit(attacker, defender, board, units):
	"""
	Attacker attacks defender.
	Returns a dict containing the following information:
		Damage dealt to attacker
		Damage dealt to defender
		The remaining health of attacker
		The remaining health of defender
	"""
	attacker_HP = attacker.hp
	defender_HP = defender.hp

	defender.attacked_by(attacker)

	if DEBUG:
		print('Attacked ' + defender.name + ' with ' + attacker.name)

	if defender.dead:
		# Move into defending unit's hex
		board[attacker.hex]['occupying'] = None
		attacker.hex = defender.hex
		board[attacker.hex]['occupying'] = attacker

		if DEBUG:
			print('Killed defending ' + str(defender))
			print('Moved attacking ' + attacker.name + ' to ' + attacker.hex)

		# Remove defender unit from units
		units[defender.p0].remove(defender)
	else:
		if DEBUG:
			print('Defending ' + str(defender) + ' HP: ' + str(defender.hp))

		# Receive retaliation damage
		attacker.retaliated_by(defender)

		if attacker.dead:
			# Remove attacker from board and units
			board[attacker.hex]['occupying'] = None
			units[attacker.p0].remove(attacker)

			if DEBUG:
				print('Attacking ' + str(attacker) + ' died in retaliation')
		else:
			if DEBUG:
				print('Attacking ' + str(attacker) + ' HP: ' + str(attacker.hp))

	attacker.exhaust()

	return {
		'attacker_HP': attacker.hp, 
		'defender_HP': defender.hp,
		'damage_to_attacker': attacker_HP - attacker.hp,
		'damage_to_defender': defender_HP - defender.hp
	}
