from stable_baselines3.common.env_checker import check_env
from la_env import LA_Env


env = LA_Env()
# It will check your custom environment and output additional warnings if needed
check_env(env)