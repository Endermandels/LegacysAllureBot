""" 
Creates the Legacy's Allure environment for training a deep reinforcement learning model.

Original code created by the Farama Foundation:
	https://github.com/Farama-Foundation/PettingZoo/blob/master/pettingzoo/classic/connect_four/connect_four.py
"""

# Training libs
import gymnasium
from gymnasium import spaces
import numpy as np

# Petting Zoo libs
from pettingzoo import AECEnv
from pettingzoo.utils import wrappers
from pettingzoo.utils.agent_selector import agent_selector

# Game libs
from game_tools.board import *
from game_tools.toolbox import *
from game_tools.unit import *
from game_tools.unit_data import *

# Number of hexes
NHEXES = 59

# Pickable unit hexes
NUNITS = NHEXES

# Actions per unit
NMOVES = NHEXES
NATTACKS = NHEXES
NACIONS_PER_UNIT = (NMOVES + NATTACKS + 1)

# Total action space
NACTION_SPACE = NUNITS * NACIONS_PER_UNIT

def env():
	env = LA_Env()
	env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
	env = wrappers.AssertOutOfBoundsWrapper(env)
	env = wrappers.OrderEnforcingWrapper(env)
	return env

class LA_Env(AECEnv):
	metadata = {
        "name": "legacys_allure_v1",
        "is_parallelizable": False
	}

	def __init__(self):
		super().__init__()

		self.agents = ["player_0", "player_1"]
		self.possible_agents = self.agents[:]

		self.action_spaces = {i: spaces.Discrete(NACTION_SPACE) for i in self.agents}
		self.observation_spaces = {
			i: spaces.Dict(
				{
					"observation": spaces.Box(
						low=0, high=1, shape=(1,), dtype=np.float64
					),
					"action_mask": spaces.Box(
						low=0, high=1, shape=(NACTION_SPACE,), dtype=np.int8
					),
				}
			)
			for i in self.agents
		}

	# Key
	# ----
	# blank space = 0
	# agent 0 = 1
	# agent 1 = 2
	# An observation is list of lists, where each list represents a row
	#
	# array([[0, 1, 1, 2, 0, 1, 0],
	#        [1, 0, 1, 2, 2, 2, 1],
	#        [0, 1, 0, 0, 1, 2, 1],
	#        [1, 0, 2, 0, 1, 1, 0],
	#        [2, 0, 0, 0, 1, 1, 0],
	#        [1, 1, 2, 1, 0, 1, 0]], dtype=int8)
	def observe(self, agent):
		# board_vals = np.array(self.board).reshape(6, 7)
		# cur_player = self.possible_agents.index(agent)
		# opp_player = (cur_player + 1) % 2

		# cur_p_board = np.equal(board_vals, cur_player + 1)
		# opp_p_board = np.equal(board_vals, opp_player + 1)

		# observation = np.stack([cur_p_board, opp_p_board], axis=2).astype(np.int8)
		legal_moves = self._legal_moves() if agent == self.agent_selection else []

		observation = [0]
		observation = np.array(observation)

		action_mask = np.zeros(NACTION_SPACE, "int8")
		for i in legal_moves:
			action_mask[i] = 1

		return {"observation": observation, "action_mask": action_mask}

	def observation_space(self, agent):
		return self.observation_spaces[agent]

	def action_space(self, agent):
		return self.action_spaces[agent]

	def _legal_moves(self):
		return [i for i in range(NACTION_SPACE) if self.valid_move(i)]

	def parse_action(self, action):
		"""
		Take an int
		Return a dict explaining the action
		"""
		parsed_action = dict()

		n_unit = action % NUNITS
		n_action = action % NACIONS_PER_UNIT

		parsed_action['unit'] = self.board.get_unit_at_hex_num(n_unit)
		parsed_action['hex'] = None

		if n_action == 0:
			parsed_action['type'] = 'pass'
		elif n_action < NMOVES:
			# TODO: Implement different movement paths
			parsed_action['type'] = 'move'
			parsed_action['hex'] = self.board.get_hex(n_action - 1) # only true when n_action is 'move'
		else:
			# TODO: Implement different attack paths
			parsed_action['type'] = 'attack'
			parsed_action['hex'] = self.board.get_hex(n_action - NMOVES - 1) # only true when n_action is 'move'

		return parsed_action

	def valid_move(self, action):
		"""
		action: int in range(NACTION_SPACE)
		returns whether the action is legal
		"""
		action = self.parse_action(action)
		unit = action['unit']
		atype = action['type']
		_hex = action['hex']

		if not unit or unit.exhausted:
			return False

		if atype == 'move':
			destinations = generate_set_destinations(self.board.hexes, unit)
			if not _hex in destinations:
				return False
		elif atype == 'attack':
			enemy = self.board.hexes[_hex]['occupying']
			if not enemy:
				return False
			enemies = attackable_enemies(self.board.hexes, unit)
			if not enemy in enemies:
				return False
		elif atype == 'pass':
			return True
		else:
			print(f'[ERROR]: Unknown action type resulting from action {action}: {atype}')
			return False

		return True

	def step(self, action):
		if self.truncations[self.agent_selection] or \
			self.terminations[self.agent_selection]:
			return self._was_dead_step(action)

		# Assert valid move
		assert self.valid_move(action), "played illegal move."

		# Update board state
		# TODO

		# Get Next Player
		next_agent = self._agent_selector.next()

		# winner = self.check_for_winner()
		winner = True # TODO: Delete

		# check if there is a winner
		if winner:
			self.rewards[self.agent_selection] += 1
			self.rewards[next_agent] -= 1
			self.terminations = {i: True for i in self.agents}

		# Switch Player
		self.agent_selection = next_agent

		# Accumulate Rewards
		self._accumulate_rewards()

	def reset(self, seed=None, options=None):
		#__RESET ENVIRONMENT__#
		self.board = Board()
		self.units = {self.agents[0]: [], self.agents[1]: []}

		# P1
		self.units[self.agents[0]] = [
			Unit(SWORDSMAN, 'D2', True, self.board.hexes),
			Unit(SWORDSMAN, 'C3', True, self.board.hexes)
		]

		# P2
		self.units[self.agents[1]] = [
			Unit(SWORDSMAN, 'D3', False, self.board.hexes)
		]

		self.round = 1
		self.p1_turn = True
		self.p1_first_turn = True # Who goes first at the start of next round

		#__RESET PLAYERS__#
		self.agents = self.possible_agents[:]
		self.rewards = {i: 0 for i in self.agents}
		self._cumulative_rewards = {name: 0 for name in self.agents}
		self.terminations = {i: False for i in self.agents}
		self.truncations = {i: False for i in self.agents}
		self.infos = {i: {} for i in self.agents}

		self._agent_selector = agent_selector(self.agents)
		self.agent_selection = self._agent_selector.reset()

#__DEBUGGING__#

def test_legal_moves():
	env = LA_Env() # TODO: Delete

	env.reset()
	legal_moves = env._legal_moves()

	parsed_moves = []
	for move in legal_moves:
		parsed_moves.append(env.parse_action(move)['type'])
	print(parsed_moves)
