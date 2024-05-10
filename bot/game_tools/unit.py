class Unit:
	def __init__(self, data, _hex, p0, board):
		# Initial Card Stats
		self.ATK = data['atk']
		self.RNG = data['rng']
		self.MOV = data['mov']
		self.HP = data['hp']

		# Current Card Stats
		self.name = data['name']
		self.atk = self.ATK
		self.mov = self.MOV
		self.hp = self.HP
		self.shield = 0
		self.exhausted = False
		self.dead = False
		self.hex = _hex

		self.p0 = p0
		board[self.hex]['occupying'] = self

		# Unused

		self.gold = data['gold']
		self.passives = data['passives']
		self.actives = data['actives']
		self.debuffs = []
		self.buffs = []

	def __repr__(self):
		return self.name + ' on ' + self.hex

	def attacked_by(self, unit, pretend=False):
		"""
		Returns whether this unit died.
		"""
		if not pretend:
			shield_save = self.shield 
			self.shield = max(self.shield - unit.atk, 0)
			self.hp -= unit.atk - (shield_save - self.shield)

			if self.hp <= 0:
				self.hp = 0 # For reward calculations
				self.dead = True
			return self.dead
		return self.hp + self.shield - unit.atk <= 0

	def retaliated_by(self, unit, pretend=False):
		"""
		Returns whether this unit died.
		"""
		return self.attacked_by(unit, pretend)

	def gain_shield(self, amount, from_center=False):
		if not from_center:
			self.shield = max(amount, self.shield)
		else:
			self.shield += amount

	def exhaust(self):
		self.exhausted = True

	def refresh(self):
		self.exhausted = False
