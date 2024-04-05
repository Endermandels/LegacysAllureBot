"""
Handles each action:
	Attack
	Move
	Pass
"""

def pass_unit(unit):
	unit.exhaust()
	print(	'Passed ' + unit.name + ' on ' + unit.hex)

def move_unit(unit, hex, board):
	prev_hex = unit.hex

	board[unit.hex]['occupying'] = None
	unit.hex = _hex
	board[unit.hex]['occupying'] = unit
	unit.exhaust()

	print(	'Moved ' + unit.name + ' from ' + prev_hex + ' to ' + unit.hex)

def attack_unit(attacker, defender, board, units):
	defender.attacked_by(attacker)

	if defender.dead:
		# Move into defending unit's hex
		board[attacker.hex]['occupying'] = None
		attacker.hex = defender.hex
		board[attacker.hex]['occupying'] = attacker

		print('Killed defending ' + defender.name)
		print('Moved attacking ' + attacker.name + ' to ' + attacker.hex)

		# Remove defender unit from units
		units[defender.p0].remove(defender)
	else:
		print('Defending ' + defender.name + ' HP: ' + str(defender.hp))

		# Receive retaliation damage
		attacker.retaliated_by(defender)

		if attacker.dead:
			print('Allied ' + attacker.name + ' died in retaliation')
			units[attacker.p0].remove(attacker)
		else:
			print('Allied ' + attacker.name + ' HP: ' + str(attacker.hp))

	attacker.exhaust()