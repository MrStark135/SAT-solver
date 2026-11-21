from sat_solver.latin_square import rules, LatinSquare
import time

def main() -> None:
	start = time.perf_counter()
	
	square = LatinSquare([ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I' ])
	print(str(square.size) + "x" + str(square.size), "square,", len(square.rules), "rules,", square.var_count_cnf, "variables")

	print(rules.solve(square, False), "\n")
	square.display()

	print("-----------------------------------")
	
	squareSet = LatinSquare(['A', 'B'])
	print(str(squareSet.size) + "x" + str(squareSet.size), "square,", len(squareSet.rules), "rules,", squareSet.var_count_cnf, "variables")
	squareSet.set_cell(('A', 0, 1))
	squareSet.set_cell(('B', 1, 1))
	print("set value:", ('B', 0, 0), "\n")

	print(rules.solve(squareSet, True), "\n")
	squareSet.display()

	end = time.perf_counter()
	print(f"\nCode took {(end-start):.6f} seconds to run")

main()