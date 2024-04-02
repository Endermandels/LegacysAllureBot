import gymnasium
from gymnasium import spaces
import numpy as np

class LA_Env(gymnasium.Env):
	def __init__(self):
		super(LA_Env, self).__init__()
		# Define action and observation space
		# They must be gym.spaces objects
		self.action_space = spaces.Discrete(1) # Pass
		self.observation_space = spaces.Box(low=0, high=500,
											shape=(1,), dtype=np.int64)
		# low -> high = how many values can be expected
		# shape = how many observation dimensions there are

	def step(self, action):

		return

	def reset(self, *, seed=None, options=None):
		self.terminated = False # When env is stopped because of failure
		self.truncated = False # When env is stopped prematurely
		return

LA_Env()
