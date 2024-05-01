"""
Handles each action:
	Attack
	Move
	Pass
"""

def pass_unit(unit, DEBUG=False):
	unit.exhaust()

	if DEBUG:
		print('Passed ' + unit.name + ' on ' + unit.hex)

def move_unit(unit, _hex, board, DEBUG=False):
	prev_hex = unit.hex

	board[unit.hex]['occupying'] = None
	unit.hex = _hex
	board[unit.hex]['occupying'] = unit
	unit.exhaust()

	if 'shield 1' in board[unit.hex]['buffs']:
		unit.gain_shield(1, from_center=True)
		board[unit.hex]['buffs'].remove('shield 1')
		if DEBUG:
			print('Unit gained a shield from the center: ' + str(board[unit.hex]['buffs']))

	if DEBUG:
		print('Moved ' + unit.name + ' from ' + prev_hex + ' to ' + unit.hex)

def attack_unit(attacker, defender, board, units=[], pretend=False, DEBUG=False):
	"""
	Attacker attacks defender.
	If not pretend:
		Returns a dict containing the following information:
			Damage dealt to attacker
			Damage dealt to defender
			The remaining health of attacker
			The remaining health of defender
	Else:
		Returns if enemy died
	"""
	attacker_HP = attacker.hp
	defender_HP = defender.hp

	dead = defender.attacked_by(attacker, pretend)

	if pretend:
		return dead

	if DEBUG:
		print('Attacked ' + defender.name + ' with ' + attacker.name)

	if dead:
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
		dead = attacker.retaliated_by(defender)

		if dead:
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
		'attacker_gold': attacker.gold,
		'defender_gold': defender.gold,
		'damage_to_attacker': attacker_HP - attacker.hp,
		'damage_to_defender': defender_HP - defender.hp
	}
