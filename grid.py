from sys import stdout
from cnf import CNF
import itertools
import time

class Grid:
	def __init__(self, size: int) -> None:
		if size > 9:
			raise ValueError("the size " + str(size) + " is too big, size <= 9 are allowed")

		# grid setup
		self.size = size
		self.var_count_cnf = self.size ** 3
		self.grid = [[ 0 for i in range(size) ] for j in range(size)]

		# mathematical representation of the rules generated dynamically depending on the size
		# this is the most basic and unoptimized approach
		self.rules = []
		for symbol in range(self.size):
			for row in range(self.size):
				
				rule_min_one_in_row = [] # AT LEAST one TRUE 
				rule_min_one_in_column = []
				rule_min_one_in_cell = []

				rule_max_one_in_row = [] # AT MOST one TRUE
				rule_max_one_in_column = []
				rule_max_one_in_cell = []
				
				for column in range(self.size):

					# by changing the order symbol, row, column we can select all in:
					rule_min_one_in_row.append(symbol * self.size ** 2 + row * self.size + column + 1) # row
					rule_min_one_in_column.append(symbol * self.size ** 2 + column * self.size + row + 1) # column
					rule_min_one_in_cell.append(column * self.size ** 2 + row * self.size + symbol + 1) # symbol

				# make NEGATED and make all the possible unordered pairs
				rule_max_one_in_row = [ list(comb) for comb in itertools.combinations([ -x for x in rule_min_one_in_row ], 2) ]
				rule_max_one_in_column = [ list(comb) for comb in itertools.combinations([ -x for x in rule_min_one_in_column ], 2) ]
				rule_max_one_in_cell = [ list(comb) for comb in itertools.combinations([ -x for x in rule_min_one_in_cell ], 2) ]

				self.rules.append(rule_min_one_in_row)
				self.rules.append(rule_min_one_in_column)
				self.rules.append(rule_min_one_in_cell)

				# chain the pairs with ANDs, i.e. add them directly to the full CNF
				for rule in rule_max_one_in_row: self.rules.append(rule)
				for rule in rule_max_one_in_column: self.rules.append(rule)
				for rule in rule_max_one_in_cell: self.rules.append(rule)

	# set some cells to a value 
	def define_values(self, values: list) -> None:
		for value in values:
			if self.symbol_allowed(value['value']):
				self.grid[value['x']][value['y']] = value['value']
			else: raise ValueError("Value " + str(value['value']) + " is not a valid symbol for this grid, size is " + str(self.size))

	# NOTE: this function will overlay the layers of symbols, so it's possible to cover a previous value
	def apply_vars_to_grid(self, vars: list) -> None:
		tmp_grid = self.vars_to_grid(vars)
		for symbol in range(self.size):
			for row in range(self.size):
				for column in range(self.size):
					# if True set to
					if tmp_grid[symbol][row][column]:
						self.grid[row][column] = symbol + 1

	# computes a 3d grid from flat list of vars
	def vars_to_grid(self, vars: list) -> list:
		if len(vars) != self.var_count_cnf:
			raise ValueError("Variables count " + str(len(vars)) + " doesn't match grid size " + str(self.size))
		tmp_grid = [[[ 0 for i in range(self.size) ] for j in range(self.size)] for k in range(self.size)]
		for var_id in range(len(vars)):
			symbol = var_id // (self.size ** 2)
			row = (var_id % (self.size ** 2)) // self.size
			column = (var_id % (self.size ** 2)) % self.size
			tmp_grid[symbol][row][column] = vars[var_id]
		return tmp_grid

	# show the layers
	def display_layers(self, vars: list) -> None:
		tmp_grid = self.vars_to_grid(vars)
		for symbol in range(len(tmp_grid)):
			stdout.write(str(symbol + 1) + ": \n")
			self.display_grid(tmp_grid[symbol])
			stdout.write("-" * self.size + "\n")

	# show a 2d grid or the self.grid
	def display_grid(self, grid_arg=None) -> None:
		grid = self.grid if grid_arg is None else grid_arg
		for row in grid:
			for cell in row:
				stdout.write(str(int(cell)))
			stdout.write("\n")

	# helpers
	def symbol_allowed(self, symbol: int) -> bool:
		if symbol > self.size or symbol < 1: return False
		else: return True

def main() -> None:
	start = time.perf_counter()
	
	grid = Grid(3)
	print(str(grid.size) + "x" + str(grid.size), "grid,", len(grid.rules), "rules,", grid.var_count_cnf, "variables")
	
	cnf = CNF(grid.var_count_cnf, grid.rules)
	vars = cnf.sat_binary()
	# vars = cnf.sat_calculate() #TODO: a faster algorithm to find a working combination
	if len(vars) > 0:
		print('SAT:', vars)
		grid.display_layers(vars)
		grid.apply_vars_to_grid(vars)
		print("GRID:")
		grid.display_grid()
	else:
		print('UNSAT')

	end = time.perf_counter()
	print(f"Code took {(end-start):.6f} seconds to run")

main()