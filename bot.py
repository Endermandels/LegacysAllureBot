from card import *
from toolbox import *
from random import randint

class Bot():
	def __init__(self, units, p1, attacker, board):
		self.units = units
		self.attacker = attacker
		self.p1 = p1
		self.board = board

		if self.p1:
			self.p_units = 'p1 units'
		else:
			self.p_units = 'p2 units'

	def __repr__(self):
		string = ''
		if self.p1:
			string = 'Bot 1'
		else:
			string = 'Bot 2'
		return string

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

		# Log previous hex before performing action
		prev_hex = action['unit'].hex

		# Perform action
		if action['name'] == 'attack':
			self._attack(action)
			print(	str(self) + ' ' +
					action['name'] + ' ' + 
					str(action['unit']))
		elif action['name'] == 'move':
			self._move(action)
			print(	str(self) + ' ' +
					action['name'] + ' from ' +
					prev_hex + ' ' + 
					str(action['unit']))
		else:
			self._pass(action)
			print(	str(self) + ' ' +
					action['name'] + ' ' + 
					str(action['unit']))
			return True

		return False

	def valid_actions(self):
		actions = []
		
		for unit in self.units[self.p_units]:
			if not unit.exhausted:
				# All units can pass
				actions.append({'name': 'pass', 'unit': unit})

				# Check if unit can Move
				possible_moves = self.can_move(unit)
				if len(possible_moves) > 0:
					for move in possible_moves:
						actions.append({'name': 'move', 
										'unit': unit, 
										'move': move})

				# Check if unit can Attack
				possible_attacks = self.can_attack(unit)

		return actions

	def decide(self, actions):
		for action in actions:
			if action['name'] == 'move' and \
				action['move'][-1] == CENTER_HEX:
				return action
		rnd = randint(0, len(actions)-1)
		return actions[rnd]

	def can_move(self, unit):
		"""
		This function returns the possible moves
		TODO: along with metadata for each move
		"""
		return generate_paths(self.board, unit)

	def can_attack(self, unit):
		return None

	def _attack(self, action):
		action['unit'].exhaust()

	def _move(self, action):
		unit = action['unit']
		self.board[unit.hex]['occupying'] = None
		unit.hex = action['move'][-1]
		self.board[unit.hex]['occupying'] = unit
		unit.exhaust()

	def _pass(self, action):
		action['unit'].exhaust()
