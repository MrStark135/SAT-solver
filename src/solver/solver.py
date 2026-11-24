from itertools import product

# this produces a list of all assignments to N variables that evaluate the clause to True
def _truth_combinations(n: int) -> list[list[bool]]:
	combs = []
	for comb in product([True, False], repeat=n):
		# exclude the "all zeros" combination
		if any(comb):
			combs.append(comb)
	return combs

def _is_negated(literal: str) -> bool:
	return literal[0] == "~"

def _var(literal: str) -> str:
	if _is_negated(literal): return literal[1:]
	return literal

# maps combinations to a clause - used with _truth_combinations yields all assignments that eval the clause to True,
# produces a dict of VAR assign values, not LITERALS
def _assign_vars(combs: list[bool], clause: list[str]) -> dict[str, bool]:
	return {
		_var(lit): _is_negated(lit)^val for lit, val in zip(clause, combs)
	}

# get literal value based on assignment dict
def _eval_literal(literal: str, assignment: dict[str, bool]) -> bool:
	return assignment[_var(literal)] ^ _is_negated(literal)

# print debug messages to analyze the internal workings of the algorithm
def solve_sat(cnf: list[list[str]], debug: bool) -> dict[str, bool] | None:
	"""Solves a CNF by recursively setting the variables of the shortest clause with N literals and reducing the CNF each step
	This algorithm produces a single assignment option that satisfies the CNF, the first one it finds, deterministic

	Args:
		cnf: CNF in format `[ ['a', '~B'], ['Ab', 'B', '~CfG'], ... ]` where variable names are any string w/~ for negation
		debug: bool if True prints debug messages, for seeing the internal workings of the algorithm

	Returns:
		dict: a dict w/format `{ 'A': True, 'CfG': False, 'AB': False, ... }`, all the varibles w/values that satisfy the CNF
		None: UNSAT, no assignment satisfies the CNF, i.e. the CNF is unsolvable
	"""
	# find shortest clause - shortest number of combinations to evaluate (2^n)
	shortest = None
	for clause in cnf:
		if shortest == None or len(clause) < len(shortest):
			shortest = clause
	# if empty CNF - return None - if it were solved, it would have returned the combination down 
	if shortest == None: return None
	
	if debug:
		print("CNF:", cnf)
		print("shortest:", shortest)

	clean_cnf = []
	for clause_tmp in cnf:
		new_clause = []
		for literal in clause_tmp:
			if literal not in new_clause:
				new_clause.append(literal)
		clean_cnf.append(new_clause)
	cnf = clean_cnf

	# reduce the CNF for all assignments of the variables of the shortest clause
	combs = _truth_combinations(len(shortest))
	for combination in combs:
		if debug: print("--Combination:", combination)
		new_cnf = _reduce_cnf(shortest, combination, cnf, debug)
		if debug: print("--Reduced CNF:", new_cnf)

		# this branch ended in conflict, check next
		if new_cnf is False: continue
		# if resolves fully just return the assignment
		elif new_cnf is True: return _assign_vars(combination, shortest)
		# if the CNF is not fully resolved, recurse and assign more variables to simplify further 
		if type(new_cnf) is list:
			if debug: print("-----------------------------")
			return_combination = solve_sat(new_cnf, debug)
		# after the recurse fully unwraps back, the return_combination is a concated dict of correct assignments {} or just a failed branch 'None'
		if return_combination is not None: return _assign_vars(combination, shortest) | return_combination

	# if no combination works, return None, failed branch, so recursion unwraps
	return None

def _reduce_cnf(set_clause: list[str], comb: list[bool], cnf: list[list[str]], debug: bool) -> list[list[str]] | bool:
	"""Reduces the original CNF by inserting the assigned variables, some clause just eval to True and get removed, while False means another
	variable from the clause needs to be True to satisfy the clause, so it gets carried over to b further processed

	Args:
		set_clause: the clause whose variables are all set to a value that evals the clause to True
		comb: the actual values to which the LITERALS will be set (not VARIABLES)
		cnf: the original CNF which will be reduced
		debug: bool if True prints debug messages, for seeing the internal workings of the algorithm

	Returns:
		list: a reduced CNF
		bool:
			False: if while evaluating there was a conflict, so the recursion can catch a bad branch,
			True: if the CNF is fully satisfied ith the assignments
	
	"""
	new_cnf = []
	assigned = _assign_vars(comb, set_clause)
	if debug: print("--Assignment:", assigned)
	for clause in cnf:

		if debug:
			print("----Start[clause]:", clause)

		# the clause picked is already satisfied - check others
		if clause == set_clause:
			if debug: print("------Calculate[clause]: clause == set_clause -> skip")
			continue

		# simplify every clause
		new_clause = []
		passed = False
		for literal in clause:

			if _var(literal) in assigned:
				if debug: print("------Calculate[literal]:", literal, '=', _eval_literal(literal, assigned))
				# if a single literal is True, it immediately satisfies the clause
				if _eval_literal(literal, assigned):
					passed = True
					break
			# if the literal is not assigned, then carry it over
			else:
				new_clause.append(literal)

		if debug:
			print("------End[passed]:", passed)
			print("------End[conflict]:", len(new_clause) == 0 and not passed)

		# check next, this one is satisfied
		if passed: continue
		# if empty clause, all literals eval to False -> CNF = False, recurse back - failed branch
		if len(new_clause) == 0:
			return False
		# if the clause didn't eval to True and is not empty, pass reduced clause down 
		if not passed:
			new_cnf.append(new_clause)

	# reurn the reduced CNF or True - CNF fully satisfied
	return new_cnf if len(new_cnf) > 0 else True