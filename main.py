from cnf import CNF
from latin_square import LatinSquare
import time

def main() -> None:
	start = time.perf_counter()
	
	grid = LatinSquare(9)
	print(str(grid.size) + "x" + str(grid.size), "grid,", len(grid.rules), "rules,", grid.var_count_cnf, "variables")
	
	cnf = CNF(grid.var_count_cnf, grid.rules)
	# vars = cnf.sat_binary() # old method, works only for small sizes
	vars = cnf.sat_dpll() # a better search algorithm
	if len(vars) > 0:
		print("SAT")
		grid.apply_vars_to_grid(vars)
		print("LATIN SQUARE:")
		grid.display_grid()
	else:
		print('UNSAT')

	end = time.perf_counter()
	print(f"Code took {(end-start):.6f} seconds to run")

main()