import solver
import itertools

# import LatinSquare ONLY for type checks, otherwise it's a circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from . import LatinSquare

def generate_cnf_rules(latinSqure: LatinSquare) -> None:
	"""Dynamically generates a list of rules (CNF) in the format required by the solver
	The rules are a mathematical expression of the constraints - i.e. how to find a valid latin square
	Args:
		latin_square: A LatinSquare object, uses `len(latin_square.symbols)` is the size of the square, symbols will also be used as variable names
	Returns:
		None: just generates a valid CNF in the format required by the solver and adds it to the LatinSquare object 
	"""
	size = latinSqure.size
	rules = []
	rule_min_one_in_cell_all = [ [[] for _cell in range(size)] for _row in range(size) ]
	for symbol in latinSqure.symbols:
		for row in range(size):
			
			rule_min_one_in_row = [] # AT LEAST one TRUE 
			rule_min_one_in_column = []

			rule_max_one_in_row = [] # AT MOST one TRUE
			rule_max_one_in_column = []
			
			for column in range(size):

				# by changing the order symbol, row, column we can select all in:
				# (this works ONLY beacause row and column are same size)
				rule_min_one_in_row.append(symbol + '.' + str(row) + '.' + str(column)) # row
				rule_min_one_in_column.append(symbol + '.' + str(column) + '.' + str(row)) # column
				# for symbols we need to push for exactly one row,col combination a single symbol, so we basically iterate over symbols
				rule_min_one_in_cell_all[row][column].append(symbol + '.' + str(row) + '.' + str(column)) # symbol

			# make NEGATED and make all the possible unordered pairs
			rule_max_one_in_row = [ list(comb) for comb in itertools.combinations([ '~' + literal for literal in rule_min_one_in_row ], 2) ]
			rule_max_one_in_column = [ list(comb) for comb in itertools.combinations([ '~' + literal for literal in rule_min_one_in_column ], 2) ]

			rules.append(rule_min_one_in_row)
			rules.append(rule_min_one_in_column)

			# chain the pairs with ANDs, i.e. add them directly to the full CNF
			for rule in rule_max_one_in_row: rules.append(rule)
			for rule in rule_max_one_in_column: rules.append(rule)

	# for rules for symbols we need to iterate again because we can't generate the pairs w/itertools.combintions until all the symbols are iterated
	for _row in rule_min_one_in_cell_all:
		for _rule in _row:
			rules.append(_rule)

			# make NEGATED and make all the possible unordered pairs
			rule_max_one_in_cell = [ list(comb) for comb in itertools.combinations([ '~' + literal for literal in _rule ], 2) ]
			for rule_max in rule_max_one_in_cell: rules.append(rule_max)

	latinSqure.rules = rules

def update_cnf_rules(latin_square: LatinSquare, symbol_x_y: tuple[str, int, int]) -> None:
	"""Updates an exisiting CNF, i.e. rules for solving the latin_square, by evaluating literals from the rules that
	are affected by the set value, symbol in location (x, y) in a the latin_square
	Args:
		latin_square: a LatinSquare Object on which the operation is performed
		symbol_x_y: symbol, x, y values that set a specific cell in the square
	Returns:
		None: replaces the rules of the latin_square object by reducing the cnf
	"""

	symbol = symbol_x_y[0]
	cell = symbol_x_y[1]
	row = symbol_x_y[2]

	if len(latin_square.rules) == 0: return

	new_rules = []
	for rule in latin_square.rules:
		new_rule = []
		passed = False
		for literal in rule:
			# get the symbol from the var name
			extract_symbol = literal.split('.')[0]
			extract_row = int(literal.split('.')[1])
			extract_cell = int(literal.split('.')[2])

			# the variable is affected by the set symbol
			if solver._var(extract_symbol) == symbol:
				if extract_row == row and extract_cell == cell:
					# if the variable is False, don't include it 
					if solver._is_negated(literal):
						continue
					# if the variable True, skip the rule, already satisfied
					else:
						passed = True
						break
				elif extract_row == row or extract_cell == cell:
					# the variable is True (negated False), skip the rule, already satisfied 
					if solver._is_negated(literal):
						passed = True
						break
					# the variable is False, don't include it
					else:
						continue
				else:
					# the variable is unaffected because doesn't match row or column, just symbol
					new_rule.append(literal)
			# the variable is affected because the symbol is set in the (row, colum)
			elif extract_row == row and extract_cell == cell:
				# the variable is True, skip the rule, already satisfied 
				if solver._is_negated(literal):
					passed = True
					break
				# the variable False (negated True), don't include it
				else:
					continue
			# the variable is completely unaffected by the set value, so just pass it on
			else:
				new_rule.append(literal)
				
		if not passed and len(new_rule) != 0: new_rules.append(new_rule)
	latin_square.rules = new_rules

def solve(latin_square: LatinSquare, debug: bool) -> str:
	"""This solves the provided latin square, optionally shows the algorithmic steps.
	Args:
		latin_square: a LatinSquare object on which to perform the solving, keep in ind to generate the rules beforehand
		debug: a bool setting verbosity - useful for visualizing the algorithm, skip for large latin_squares as introduces delays for printing
	Returns:
		str: 'SAT', 'UNSAT' string, the solution is handed to the latin_square object, this is just a quick feedback
	"""
	assignments = solver.solve_sat(latin_square.rules, debug)
	if assignments is None: return "UNSAT"

	for var, setTrue in assignments.items():
		if not setTrue: continue

		symbol = var.split('.')[0]
		row = int(var.split('.')[1])
		cell = int(var.split('.')[2])

		if latin_square.display_square[row][cell] is not None:
			return "INVALID SAT"
		latin_square.display_square[row][cell] = symbol

	return "SAT"