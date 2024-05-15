""" 
Creates the Legacy's Allure environment for training a deep reinforcement learning model.

Original code created by the Farama Foundation:
	https://github.com/Farama-Foundation/PettingZoo/blob/master/pettingzoo/classic/connect_four/connect_four.py
"""

# Training libs
import gymnasium
from gymnasium import spaces
import numpy as np
import time

# Petting Zoo libs
from pettingzoo import AECEnv
from pettingzoo.utils import wrappers
from pettingzoo.utils.agent_selector import agent_selector

# Game libs
from game_tools.board import *
from game_tools.toolbox import *
from game_tools.unit import *
from game_tools.unit_data import *
from game_tools.action import *

"""
Actions per unit:
	0. Take Center
		Move to center (if empty)
		Attack unit on center (if enemy)
		Pass on center (if ally)
		Otherwise, invalid action
	1. Attack
		Attack an enemy (if able)
		Otherwise, invalid action
	2. Move to Attack
		Move next to an enemy (if able)
		Otherwise, invalid action
	3. Reposition
		Move to a spot out of enemy reach, but close to the center hex (if able)
		Otherwise, invalid action
	4. Stall
		Pass (prefer lower gold, or insignificant to play)
"""

# Number of hexes (and units)
NHEXES = 59

# Actions per unit
NACIONS_PER_UNIT = 5

# Total action space
NACTION_SPACE = NHEXES * NACIONS_PER_UNIT

def env(DEBUG=False, vs_human=False):
	env = LA_Env(DEBUG=DEBUG, vs_human=vs_human)
	env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
	env = wrappers.AssertOutOfBoundsWrapper(env)
	env = wrappers.OrderEnforcingWrapper(env)
	return env

class LA_Env(AECEnv):
	metadata = {
		"name": "legacys_allure_v3",
		"is_parallelizable": False
	}

	def __init__(self, DEBUG=False, vs_human=False):
		super().__init__()

		self.DEBUG = DEBUG
		self.vs_human = vs_human

		self.agents = ["player_0", "player_1"]
		self.possible_agents = self.agents[:]

		self.action_spaces = {i: spaces.Discrete(NACTION_SPACE) for i in self.agents}
		self.observation_spaces = {
			i: spaces.Dict(
				{
					"observation": spaces.Box(
						low=0, high=1000000, shape=(5+NHEXES,), dtype=np.int8
					),
					"action_mask": spaces.Box(
						low=0, high=1, shape=(NACTION_SPACE,), dtype=np.int8
					),
				}
			)
			for i in self.agents
		}

	"""
	Observations:
		is attacker
		is going first next round
		current round
		allied gold remaining
		enemy gold remaining
		units in each hex:
			0 for none
			1xx for ally with xx effective health
			2xx for exhausted ally
			3xx for enemy
			4xx for exhausted enemy
	"""
	def observe(self, agent):
		legal_moves = self._legal_moves() if agent == self.agent_selection else []

		action_mask = np.zeros(NACTION_SPACE, "int8")
		for i in legal_moves:
			action_mask[i] = 1

		#_______________OBSERVATIONS_______________#

		allied_gold_remaining, enemy_gold_remaining = \
			gold_remaining(self.units, self.is_p0_agent())

		# TODO: add buffs on hexes to observation (shield 1 in center)

		observation = [
			int(self.is_p0_agent()),
			int(self.p0_first_turn == self.is_p0_agent()),
			self.round, 
			allied_gold_remaining, 
			enemy_gold_remaining
		]
		observation += observable_units(self.board, self.is_p0_agent())
		observation = np.array(observation)

		return {"observation": observation, "action_mask": action_mask}

	def observation_space(self, agent):
		return self.observation_spaces[agent]

	def action_space(self, agent):
		return self.action_spaces[agent]

	def is_p0_agent(self):
		return self.agent_selection == 'player_0'

	def _legal_moves(self):
		return [i for i in range(NACTION_SPACE) if self.valid_move(i)]

	def parse_action(self, action):
		"""
		Take an int
		Return a dict explaining the action
		"""

		actions = {
			0: 'center',
			1: 'attack',
			2: 'move',
			3: 'reposition',
			4: 'stall'
		}

		parsed_action = dict()

		n_unit = action // NACIONS_PER_UNIT
		n_action = action % NACIONS_PER_UNIT

		parsed_action['unit'] = None
		parsed_action['type'] = None

		# If unit either does not exist, is exhausted, or is an enemy unit, invalid move
		unit = self.board.get_unit_at_hex_num(n_unit)
		if not unit or unit.exhausted or self.is_p0_agent() != unit.p0:
			return parsed_action
		
		parsed_action['unit'] = unit
		parsed_action['type'] = actions[n_action]

		return parsed_action

	def human_action(self):
		"""
		Valid unit hex includes: x9, X9
		Valid action includes: center, attack, move, reposition, stall
		"""
		human_input = input("Enter '<unit hex> <action>': ").split()
		print()

		if len(human_input) != 2:
			return -1

		actions = {
			'center': 		0,
			'attack': 		1,
			'move': 		2,
			'reposition': 	3,
			'stall': 		4
		}

		unit_hex = human_input[0].upper()
		act_type = human_input[1].lower()
		if not unit_hex in self.board.HEX_LIST or not act_type in actions.keys():
			return -1

		n_hex = self.board.get_nhex(unit_hex)
		n_unit = n_hex * NACIONS_PER_UNIT
		
		return n_unit + actions[act_type]

	def valid_move(self, action):
		"""
		action: int in range(NACTION_SPACE)
		returns whether the action is legal
		"""
		if action < 0:
			# For when the user is trying to perform an invalid action
			return False

		action = self.parse_action(action)
		unit = action['unit']
		act_type = action['type']

		if not unit:
			return False

		if act_type == 'center':
			# Pass on center if already there
			if unit.hex == self.board.CENTER_HEX:
				return True

			# Move to center if possible
			destinations = generate_set_destinations(self.board.hexes, unit)
			if self.board.CENTER_HEX in destinations:
				return True

			# Attack enemy on center if possible
			enemies = attackable_enemies(self.board.hexes, unit)
			for enemy in enemies:
				if enemy.hex == self.board.CENTER_HEX:
					return True
			return False
		if act_type == 'attack':
			# Check if there are enemies to attack
			enemies = attackable_enemies(self.board.hexes, unit)
			return len(enemies) > 0
		if act_type == 'move':
			# Move towards enemies
			destinations = generate_set_destinations(self.board.hexes, unit)
			for h in destinations:
				enemies = attackable_enemies(self.board.hexes, unit, _hex=h)
				if len(enemies) > 0:
					return True
			return False
		if act_type == 'reposition':
			# Move away from enemies
			destinations = generate_set_destinations(self.board.hexes, unit)
			for h in destinations:
				enemies = attackable_enemies(self.board.hexes, unit, _hex=h)
				if len(enemies) == 0:
					return True
			return False
		if act_type == 'stall':
			# Pass with unit
			return True

		print(f'[ERROR]: Unknown action type resulting from action {action}: {act_type}')
		return False

	def perform_action(self, action):
		"""
		Takes in a parsed action dict.
		Returns a dict with the following information:
		"""
		if self.DEBUG:
			print(f'[{self.agent_selection}] Turn')

		unit = action['unit']
		atype = action['type']

		passed = False

		# Calculate reward per outcome of each action
		if atype == 'move':
			move_unit(unit, _hex, self.board.hexes, DEBUG=self.DEBUG)
			# dist = dist_to_hex(_hex, self.board.CENTER_HEX, self.board.hexes)
		elif atype == 'attack':
			results = attack_unit(	unit, 
									self.board.hexes[_hex]['occupying'], 
									self.board.hexes, 
									units=self.units,
									DEBUG=self.DEBUG)
			attacker_HP = results['attacker_HP']
			defender_HP = results['defender_HP']
			attacker_gold = results['attacker_gold']
			defender_gold = results['defender_gold']
			damage_to_attacker = results['damage_to_attacker']
			damage_to_defender = results['damage_to_defender']
			
			# Reward killing enemy, punish killing ally
			rew_amount = 0
			if defender_HP <= 0:
				rew_amount = 5*defender_gold
			elif attacker_HP <= 0:
				rew_amount = damage_to_defender*defender_gold - \
				damage_to_attacker*attacker_gold + 2
			else:
				rew_amount = damage_to_defender*defender_gold - \
					damage_to_attacker*attacker_gold + 10

			self.rewards[self.agent_selection] += rew_amount
			if self.DEBUG and rew_amount != 0:
				print(f'Attack Reward: {rew_amount}')

		elif atype == 'pass':
			pass_unit(unit, DEBUG=self.DEBUG)
			passed = True

		if self.DEBUG:
			time.sleep(0.5)

		return passed

	def get_winner(self):
		center_unit = self.board.hexes[self.board.CENTER_HEX]['occupying']

		# Attacker wins by controling the center at end of game
		if center_unit and center_unit.p0:
			return (self.agents[0], self.agents[1])

		# Defender wins otherwise
		return (self.agents[1], self.agents[0])

	def step(self, action):
		if self.truncations[self.agent_selection] or \
			self.terminations[self.agent_selection]:
			return self._was_dead_step(action)

		# Assert valid move
		assert self.valid_move(action), "played illegal move."

		#________________Update board state________________#

		# Player makes a move
		passed = self.perform_action(self.parse_action(action))
		if not passed:
			self.p0_first_turn = not self.is_p0_agent()

		# Rewards killing enemies
		allied_gold_remaining, enemy_gold_remaining = \
			gold_remaining(self.units, self.is_p0_agent())
		rew_amount = self.starting_gold[not self.is_p0_agent()] - enemy_gold_remaining
		self.rewards[self.agent_selection] += rew_amount
		if self.DEBUG and rew_amount != 0:
			print(f'Gold Reward: {rew_amount}')

		# If all units exhausted
		if all_units_exhausted(self.units):
			# Go to next round
			end_of_round(self.units)
			self.round += 1
	
			if self.DEBUG:
				print(f'\nGoing to Round {str(self.round)}\n')

			# Check if game ends
			if self.round == 8:
				winner, loser = self.get_winner()

				# Rewards

				# Only reward winning by both players acting as attacker
				center_unit = self.board.hexes[self.board.CENTER_HEX]['occupying']
				if center_unit and center_unit.p0 == (winner == 'player_0'):
					self.rewards[winner] += 100
				else:
					self.rewards[winner] -= 100
				self.rewards[loser] -= 100

				if self.DEBUG:
					print(f'[{winner}] Wins!')
					print(f'Winner Reward: {self.rewards[winner]}')
					print(f'Loser Reward: {self.rewards[loser]}')
					print()

				# Stop game
				self.terminations = {i: True for i in self.agents}

				# Accumulate Rewards
				self._accumulate_rewards()
				return

			# Check if current player goes first
			if self.p0_first_turn != self.is_p0_agent() and \
				can_use_unit(self.units, not self.is_p0_agent()):
				
				# Switch Player
				self.agent_selection = self._agent_selector.next()
		elif can_use_unit(self.units, not self.is_p0_agent()):
			# Switch Player
			self.agent_selection = self._agent_selector.next()

		# Accumulate Rewards
		self._accumulate_rewards()


	def reset(self, seed=None, options=None):
		#_________________RESET ENVIRONMENT_________________#

		self.board = Board()
		self.units = dict()

		# P0 (Attacker) (TRUE)
		self.units[True] = [
			Unit(SWORDSMAN, 'D5', True, self.board.hexes),
			Unit(SWORDSMAN, 'F5', True, self.board.hexes)
		]

		# P1 (Defender) (FALSE)
		self.units[False] = [
			Unit(SWORDSMAN, 'E2', False, self.board.hexes)
		]

		# Store the starting gold of each kingdom
		p0_starting_gold, p1_starting_gold = \
			gold_remaining(self.units, True)
		self.starting_gold = { True: p0_starting_gold, False: p1_starting_gold }

		self.round = 1
		self.p0_first_turn = True # Who goes first at the start of next round

		#___________________RESET PLAYERS___________________#

		self.agents = self.possible_agents[:]
		self.rewards = {i: 0 for i in self.agents}
		self._cumulative_rewards = {name: 0 for name in self.agents}
		self.terminations = {i: False for i in self.agents}
		self.truncations = {i: False for i in self.agents}
		self.infos = {i: {} for i in self.agents}

		self._agent_selector = agent_selector(self.agents)
		self.agent_selection = self._agent_selector.reset()

#______________________DEBUGGING______________________#

def test_legal_moves():
	env = LA_Env()

	env.reset()
	legal_moves = env._legal_moves()

	parsed_moves = []
	for move in legal_moves:
		parsed_moves.append(env.parse_action(move))
	sorted_list = sorted(parsed_moves, key=lambda d: str(d['unit']))

	unit_lists = []
	num_unit_lists = -1

	prev_unit = None
	for action in sorted_list:
		if prev_unit != action['unit']:
			prev_unit = action['unit']
			unit_lists.append([])
			num_unit_lists += 1
		unit_lists[num_unit_lists].append(action)

	for unit_list in unit_lists:
		sorted_unit_list = sorted(unit_list, key=lambda d: str(d['type']))
		for action in sorted_unit_list:
			print(action)
		print()

# test_legal_moves()