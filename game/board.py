'''
Each space contains:
	A list of adjacent spaces
	A list of buffs
	An occupying unit, if any
'''

board = {
	'A1': {'adj spaces': ['A2', 'B1'], 'buffs': [], 'occupying': None},
	'A2': {'adj spaces': ['A3', 'B2', 'B1', 'A1'], 'buffs': [], 'occupying': None},
	'A3': {'adj spaces': ['A4', 'B3', 'B2', 'A2'], 'buffs': [], 'occupying': None},
	'A4': {'adj spaces': ['A5', 'B4', 'B3', 'A3'], 'buffs': [], 'occupying': None},
	'A5': {'adj spaces': ['A6', 'B5', 'B4', 'A4'], 'buffs': [], 'occupying': None},
	'A6': {'adj spaces': ['A7', 'B6', 'B5', 'A5'], 'buffs': [], 'occupying': None},
	'A7': {'adj spaces': ['B6', 'A6'], 'buffs': [], 'occupying': None},

	'B1': {'adj spaces': ['A1', 'A2', 'B2', 'C2', 'C1'], 'buffs': [], 'occupying': None},
	'B2': {'adj spaces': ['A2', 'A3', 'B3', 'C3', 'C2', 'B1'], 'buffs': [], 'occupying': None},
	'B3': {'adj spaces': ['A3', 'A4', 'B4', 'C4', 'C3', 'B2'], 'buffs': [], 'occupying': None},
	'B4': {'adj spaces': ['A4', 'A5', 'B5', 'C5', 'C4', 'B3'], 'buffs': [], 'occupying': None},
	'B5': {'adj spaces': ['A5', 'A6', 'B6', 'C6', 'C5', 'B4'], 'buffs': [], 'occupying': None},
	'B6': {'adj spaces': ['A6', 'A7', 'C7', 'C6', 'B5'], 'buffs': [], 'occupying': None},

	'C1': {'adj spaces': ['B1', 'C2', 'D1'], 'buffs': [], 'occupying': None},
	'C2': {'adj spaces': ['B1', 'B2', 'C3', 'D2', 'D1', 'C1'], 'buffs': [], 'occupying': None},
	'C3': {'adj spaces': ['B2', 'B3', 'C4', 'D3', 'D2', 'C2'], 'buffs': [], 'occupying': None},
	'C4': {'adj spaces': ['B3', 'B4', 'C5', 'D4', 'D3', 'C3'], 'buffs': [], 'occupying': None},
	'C5': {'adj spaces': ['B4', 'B5', 'C6', 'D5', 'D4', 'C4'], 'buffs': [], 'occupying': None},
	'C6': {'adj spaces': ['B5', 'B6', 'C7', 'D6', 'D5', 'C5'], 'buffs': [], 'occupying': None},
	'C7': {'adj spaces': ['B6', 'C6', 'D6'], 'buffs': [], 'occupying': None},

	'D1': {'adj spaces': ['C1', 'C2', 'D2', 'E2', 'E1'], 'buffs': [], 'occupying': None},
	'D2': {'adj spaces': ['C2', 'C3', 'D3', 'E3', 'E2', 'D1'], 'buffs': [], 'occupying': None},
	'D3': {'adj spaces': ['C3', 'C4', 'D4', 'E4', 'E3', 'D2'], 'buffs': [], 'occupying': None},
	'D4': {'adj spaces': ['C4', 'C5', 'D5', 'E5', 'E4', 'D3'], 'buffs': [], 'occupying': None},
	'D5': {'adj spaces': ['C5', 'C6', 'D6', 'E6', 'E5', 'D4'], 'buffs': [], 'occupying': None},
	'D6': {'adj spaces': ['C6', 'C7', 'E7', 'E6', 'D5'], 'buffs': [], 'occupying': None},

	'E1': {'adj spaces': ['D1', 'E2', 'F1'], 'buffs': [], 'occupying': None},
	'E2': {'adj spaces': ['D1', 'D2', 'E3', 'F2', 'F1', 'E1'], 'buffs': [], 'occupying': None},
	'E3': {'adj spaces': ['D2', 'D3', 'E4', 'F3', 'F2', 'E2'], 'buffs': [], 'occupying': None},
	'E4': {'adj spaces': ['D3', 'D4', 'E5', 'F4', 'F3', 'E3'], 'buffs': [], 'occupying': None},
	'E5': {'adj spaces': ['D4', 'D5', 'E6', 'F5', 'F4', 'E4'], 'buffs': [], 'occupying': None},
	'E6': {'adj spaces': ['D5', 'D6', 'E7', 'F6', 'F5', 'E5'], 'buffs': [], 'occupying': None},
	'E7': {'adj spaces': ['D6', 'E6', 'F6'], 'buffs': [], 'occupying': None},

	'F1': {'adj spaces': ['E1', 'E2', 'F2', 'G2', 'G1'], 'buffs': [], 'occupying': None},
	'F2': {'adj spaces': ['E2', 'E3', 'F3', 'G3', 'G2', 'F1'], 'buffs': [], 'occupying': None},
	'F3': {'adj spaces': ['E3', 'E4', 'F4', 'G4', 'G3', 'F2'], 'buffs': [], 'occupying': None},
	'F4': {'adj spaces': ['E4', 'E5', 'F5', 'G5', 'G4', 'F3'], 'buffs': [], 'occupying': None},
	'F5': {'adj spaces': ['E5', 'E6', 'F6', 'G6', 'G5', 'F4'], 'buffs': [], 'occupying': None},
	'F6': {'adj spaces': ['E6', 'E7', 'G7', 'G6', 'F5'], 'buffs': [], 'occupying': None},

	'G1': {'adj spaces': ['F1', 'G2', 'H1'], 'buffs': [], 'occupying': None},
	'G2': {'adj spaces': ['F1', 'F2', 'G3', 'H2', 'H1', 'G1'], 'buffs': [], 'occupying': None},
	'G3': {'adj spaces': ['F2', 'F3', 'G4', 'H3', 'H2', 'G2'], 'buffs': [], 'occupying': None},
	'G4': {'adj spaces': ['F3', 'F4', 'G5', 'H4', 'H3', 'G3'], 'buffs': [], 'occupying': None},
	'G5': {'adj spaces': ['F4', 'F5', 'G6', 'H5', 'H4', 'G4'], 'buffs': [], 'occupying': None},
	'G6': {'adj spaces': ['F5', 'F6', 'G7', 'H6', 'H5', 'G5'], 'buffs': [], 'occupying': None},
	'G7': {'adj spaces': ['F6', 'G6', 'H6'], 'buffs': [], 'occupying': None},

	'H1': {'adj spaces': ['G1', 'G2', 'H2', 'I2', 'I1'], 'buffs': [], 'occupying': None},
	'H2': {'adj spaces': ['G2', 'G3', 'H3', 'I3', 'I2', 'H1'], 'buffs': [], 'occupying': None},
	'H3': {'adj spaces': ['G3', 'G4', 'H4', 'I4', 'I3', 'H2'], 'buffs': [], 'occupying': None},
	'H4': {'adj spaces': ['G4', 'G5', 'H5', 'I5', 'I4', 'H3'], 'buffs': [], 'occupying': None},
	'H5': {'adj spaces': ['G5', 'G6', 'H6', 'I6', 'I5', 'H4'], 'buffs': [], 'occupying': None},
	'H6': {'adj spaces': ['G6', 'G7', 'I7', 'I6', 'H5'], 'buffs': [], 'occupying': None},

	'I1': {'adj spaces': ['I2', 'H1'], 'buffs': [], 'occupying': None},
	'I2': {'adj spaces': ['I3', 'H2', 'H1', 'I1'], 'buffs': [], 'occupying': None},
	'I3': {'adj spaces': ['I4', 'H3', 'H2', 'I2'], 'buffs': [], 'occupying': None},
	'I4': {'adj spaces': ['I5', 'H4', 'H3', 'I3'], 'buffs': [], 'occupying': None},
	'I5': {'adj spaces': ['I6', 'H5', 'H4', 'I4'], 'buffs': [], 'occupying': None},
	'I6': {'adj spaces': ['I7', 'H6', 'H5', 'I5'], 'buffs': [], 'occupying': None},
	'I7': {'adj spaces': ['H6', 'I6'], 'buffs': [], 'occupying': None}
}

p1_draft_board = {
	'A1': {'adj spaces': ['A2', 'B1'], 'buffs': [], 'occupying': None},
	'A2': {'adj spaces': ['A3', 'B2', 'B1', 'A1'], 'buffs': [], 'occupying': None},
	'B1': {'adj spaces': ['A1', 'A2', 'B2', 'C2', 'C1'], 'buffs': [], 'occupying': None},
	'B2': {'adj spaces': ['A2', 'A3', 'B3', 'C3', 'C2', 'B1'], 'buffs': [], 'occupying': None},
	'C1': {'adj spaces': ['B1', 'C2', 'D1'], 'buffs': [], 'occupying': None},
	'C2': {'adj spaces': ['B1', 'B2', 'C3', 'D2', 'D1', 'C1'], 'buffs': [], 'occupying': None},
	'D1': {'adj spaces': ['C1', 'C2', 'D2', 'E2', 'E1'], 'buffs': [], 'occupying': None},
	'D2': {'adj spaces': ['C2', 'C3', 'D3', 'E3', 'E2', 'D1'], 'buffs': [], 'occupying': None},
	'E1': {'adj spaces': ['D1', 'E2', 'F1'], 'buffs': [], 'occupying': None},
	'E2': {'adj spaces': ['D1', 'D2', 'E3', 'F2', 'F1', 'E1'], 'buffs': [], 'occupying': None},
	'F1': {'adj spaces': ['E1', 'E2', 'F2', 'G2', 'G1'], 'buffs': [], 'occupying': None},
	'F2': {'adj spaces': ['E2', 'E3', 'F3', 'G3', 'G2', 'F1'], 'buffs': [], 'occupying': None},
	'G1': {'adj spaces': ['F1', 'G2', 'H1'], 'buffs': [], 'occupying': None},
	'G2': {'adj spaces': ['F1', 'F2', 'G3', 'H2', 'H1', 'G1'], 'buffs': [], 'occupying': None},
	'H1': {'adj spaces': ['G1', 'G2', 'H2', 'I2', 'I1'], 'buffs': [], 'occupying': None},
	'H2': {'adj spaces': ['G2', 'G3', 'H3', 'I3', 'I2', 'H1'], 'buffs': [], 'occupying': None},
	'I1': {'adj spaces': ['I2', 'H1'], 'buffs': [], 'occupying': None},
	'I2': {'adj spaces': ['I3', 'H2', 'H1', 'I1'], 'buffs': [], 'occupying': None}
}

p2_draft_board = {
	'A6': {'adj spaces': ['A7', 'B6', 'B5', 'A5'], 'buffs': [], 'occupying': None},
	'A7': {'adj spaces': ['B6', 'A6'], 'buffs': [], 'occupying': None},
	'B5': {'adj spaces': ['A5', 'A6', 'B6', 'C6', 'C5', 'B4'], 'buffs': [], 'occupying': None},
	'B6': {'adj spaces': ['A6', 'A7', 'C7', 'C6', 'B5'], 'buffs': [], 'occupying': None},
	'C6': {'adj spaces': ['B5', 'B6', 'C7', 'D6', 'D5', 'C5'], 'buffs': [], 'occupying': None},
	'C7': {'adj spaces': ['B6', 'C6', 'D6'], 'buffs': [], 'occupying': None},
	'D5': {'adj spaces': ['C5', 'C6', 'D6', 'E6', 'E5', 'D4'], 'buffs': [], 'occupying': None},
	'D6': {'adj spaces': ['C6', 'C7', 'E7', 'E6', 'D5'], 'buffs': [], 'occupying': None},
	'E6': {'adj spaces': ['D5', 'D6', 'E7', 'F6', 'F5', 'E5'], 'buffs': [], 'occupying': None},
	'E7': {'adj spaces': ['D6', 'E6', 'F6'], 'buffs': [], 'occupying': None},
	'F5': {'adj spaces': ['E5', 'E6', 'F6', 'G6', 'G5', 'F4'], 'buffs': [], 'occupying': None},
	'F6': {'adj spaces': ['E6', 'E7', 'G7', 'G6', 'F5'], 'buffs': [], 'occupying': None},
	'G6': {'adj spaces': ['F5', 'F6', 'G7', 'H6', 'H5', 'G5'], 'buffs': [], 'occupying': None},
	'G7': {'adj spaces': ['F6', 'G6', 'H6'], 'buffs': [], 'occupying': None},
	'H5': {'adj spaces': ['G5', 'G6', 'H6', 'I6', 'I5', 'H4'], 'buffs': [], 'occupying': None},
	'H6': {'adj spaces': ['G6', 'G7', 'I7', 'I6', 'H5'], 'buffs': [], 'occupying': None},
	'I6': {'adj spaces': ['I7', 'H6', 'H5', 'I5'], 'buffs': [], 'occupying': None},
	'I7': {'adj spaces': ['H6', 'I6'], 'buffs': [], 'occupying': None}
}