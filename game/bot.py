from toolbox import *
from random import randint

class Bot():
	def __init__(self, units, p1, attacker, board):
		self.units = units
		self.attacker = attacker
		self.p1 = p1
		self.board = board

		if self.p1:
			self.allied_units = 'p1 units'
			self.enemy_units = 'p2 units'
			self.name = '[Bot 1]'
		else:
			self.allied_units = 'p2 units'
			self.enemy_units = 'p1 units'
			self.name = '[Bot 2]'

	def do_action(self):
		"""
		Returns whether the action was a pass
		"""

		# Determine valid actions
		actions = self.valid_actions()
		if len(actions) < 1:
			return False

		# Decide on best action
		action = self.decide(actions)

		# Perform action
		if action['name'] == 'attack':
			self._attack(action)
		elif action['name'] == 'move':
			self._move(action)
		else:
			self._pass(action)
			return True

		return False

	def valid_actions(self):
		actions = []
		
		for unit in self.units[self.allied_units]:
			if not unit.exhausted:
				# All units can pass
				actions.append({'name': 'pass', 'unit': unit})

				# Check if unit can Move
				possible_moves = self.can_move(unit)
				for move in possible_moves:
					actions.append({'name': 'move', 
									'unit': unit, 
									'move': move})

				# Check if unit can Attack
				possible_attacks = self.can_attack(unit)
				for defender in possible_attacks:
					actions.append({'name': 'attack',
									'unit': unit,
									'enemy': defender})

		return actions

	def decide(self, actions):
		rnd = randint(0, len(actions)-1)
		return actions[rnd]

	def can_move(self, unit):
		"""
		Returns the possible moves
		TODO: along with metadata for each move
		"""
		return generate_paths(self.board, unit)

	def can_attack(self, unit):
		"""
		Returns the possible attacks
		TODO: along with the movement metadata
		"""
		return attackable_hexes(self.board, unit)

	def _attack(self, action):
		unit = action['unit']
		enemy = action['enemy']

		print(	self.name + ' Attacked enemy ' +
				enemy.name + ' on ' + enemy.hex + ' with allied ' +
				unit.name + ' from ' + unit.hex)

		enemy.attacked_by(unit)
		if enemy.dead:
			# Move into enemy unit's hex
			self.board[unit.hex]['occupying'] = None
			unit.hex = enemy.hex
			self.board[unit.hex]['occupying'] = unit
			print('Killed enemy ' + enemy.name)
			print('Moved allied ' + unit.name + ' to ' + unit.hex)

			# Remove enemy unit from units
			self.units[self.enemy_units].remove(enemy)
		else:
			print('Enemy ' + enemy.name + ' HP: ' + str(enemy.hp))

			# Receive retaliation damage
			unit.retaliated_by(enemy)

			if unit.dead:
				print('Allied ' + unit.name + ' died in retaliation')
				self.units[self.allied_units].remove(unit)
			else:
				print('Allied ' + unit.name + ' HP: ' + str(unit.hp))

		action['unit'].exhaust()

	def _move(self, action):
		unit = action['unit']
		prev_hex = unit.hex

		self.board[unit.hex]['occupying'] = None
		unit.hex = action['move'][-1]
		self.board[unit.hex]['occupying'] = unit
		unit.exhaust()

		print(	self.name + ' Moved ' + unit.name + ' from ' +
				prev_hex + ' to ' + unit.hex)

	def _pass(self, action):
		unit = action['unit']
		unit.exhaust()
		print(	self.name + ' Passed ' + 
				unit.name + ' on ' + unit.hex)
