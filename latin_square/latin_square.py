import itertools
from sys import stdout
from sat_solver import solver
from . import rules

class LatinSquare:
	def __init__(self, symbols: list[str]) -> None:
		# square setup
		self.size = len(symbols)
		self.symbols = symbols
		self.var_count_cnf = self.size ** 3
		self.display_square = self.clear_square()
		self.rules = []
		rules.generate_cnf_rules(self)

	def clear_square(self) -> list[list[str | None]]:
		return [[None for _cell in range(self.size)] for _row in range(self.size)]

	def set_cell(self, symbol_x_y: tuple[str, int, int]) -> None:
		symbol = symbol_x_y[0]
		cell = symbol_x_y[1]
		row = symbol_x_y[2]

		# check if valid symbol, x, y provided
		if symbol not in self.symbols or row >= self.size or cell >= self.size:
			raise ValueError("Symbol: " + symbol + ", x: " + str(cell) + ", y: "+ str(cell) + " is invalid")
		# update the display square
		self.display_square[row][cell] = symbol
		rules.update_cnf_rules(self, symbol_x_y)

	def display(self) -> None:
		# usually the symbols will be single characters, but in case they are not, this ensures proper tabular look
		longest = max((len(sym) for sym in self.symbols), default=0)

		for row in self.display_square:
			for cell in row:
				disp = cell if cell is not None else '/'
				stdout.write(str(disp) + " " * (longest - len(disp)))
			stdout.write("\n")