# Training libs
import gymnasium
from gymnasium import spaces
import numpy as np

# Game libs
from game_tools.board import *
from game_tools.toolbox import *
from game_tools.unit import *
from game_tools.unit_data import *

NHEXES = 59

class LA_Env(gymnasium.Env):
	def __init__(self):
		super(LA_Env, self).__init__()
		# Action Space = Choose_Unit * (Move + Attack + Pass)
		self.action_space = spaces.Discrete(NHEXES * (NHEXES + NHEXES + 1)) 
		# low -> high = how many values can be expected
		# shape = how many observation dimensions there are
		self.observation_space = spaces.Box(low=0, high=500,
											shape=(1,), dtype=np.float64)

	def step(self, action):

		# TODO: Learn action_space masking

		# Game Loop

		# Reward

		# Observation
		self.observation = [2.0]
		self.observation = np.array(self.observation)

		info = {}
		return self.observation, self.reward, self.terminated, self.truncated, info

	def reset(self, *, seed=None, options=None):
		self.terminated = False # When env is stopped because of failure
		self.truncated = False # When env is stopped prematurely

		# Game Setup
		self.board = Board()
		self.units = {'p1 units': [], 'p2 units': []}

		# P1
		self.units['p1 units'] = [
			Unit(SWORDSMAN, 'D2', True, self.board.hexes)
		]

		# P2
		self.units['p2 units'] = [
			Unit(SWORDSMAN, 'D5', False, self.board.hexes)
		]

		# Reward
		self.reward = 0

		# Observation

		self.observation = [2.0]
		self.observation = np.array(self.observation)
		
		
		info = {}
		return self.observation, info

LA_Env()
