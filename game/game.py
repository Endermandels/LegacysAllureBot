from board import *
from unit import Unit
from unit_data import *
from toolbox import *
from bot import Bot

def setup(data):
	units = data['units']

	# P1
	units['p1 units'] = [
		Unit(SWORDSMAN, 'E4', True, board)
	]

	# P2
	units['p2 units'] = [
		Unit(SWORDSMAN, 'E3', False, board)
	]

	data['bot1'] = Bot(units, True, True, board)
	data['bot2'] = Bot(units, False, False, board)

def gameloop(data):
	units = data['units']
	bot1 = data['bot1']
	bot2 = data['bot2']

	_round = 1
	p1_turn = bot1.attacker
	p1_first_turn = True # Who goes first at the start of next round

	while _round < 8:
		print()
		print('--------------- ROUND ' + str(_round) + ' ---------------')
		print()

		p1_turn = p1_first_turn

		while not all_units_exhausted(units):
			if p1_turn:
				passed = bot1.do_action()
				if not passed:
					p1_first_turn = False
			else:
				passed = bot2.do_action()
				if not passed:
					p1_first_turn = True

			p1_turn = not p1_turn
			print()

		end_of_round(units)
		_round += 1

def results(data):
	bot1 = data['bot1']
	bot2 = data['bot2']

	center_unit = board[CENTER_HEX]['occupying']

	if center_unit:
		if center_unit.p1:
			print(bot1.name + ' wins!')
		else:
			print(bot2.name + ' wins!')
	else:
		if bot1.attacker:
			print(bot2.name + ' wins!')
		else:
			print(bot1.name + ' wins!')

def main():
	data = {'units': {'p1 units': [], 'p2 units': []}}
	setup(data)
	gameloop(data)
	results(data)

if __name__ == '__main__':
	main()