class CNF:
	def __init__(self, var_count: int, clauses: list) -> None:

		# check the validity of the input data before creating a CNF
		if var_count <= 0: raise ValueError("Number of variables " + str(var_count) + " not allowed")
		for clause in clauses:
			for var in clause:
				if abs(var) > var_count or var == 0:
					raise ValueError("Variable " + str(var) + " out of range defined by " + str(var_count))

		self.var_count = var_count
		self.clauses = sorted(clauses, key=len)

	def eval_cnf(self, values) -> bool:
		if len(values) != self.var_count:
			raise ValueError("Provided too many/little values for variable evaluation: " + str(len(values)) + " != " + str(self.var_count))
		result = True
		for clause in self.clauses:
			result = result and self.eval_clause(clause, values)
			if result is False: break # if a single term is False, the result will be False regardless of the other terms
		return result

	def eval_clause(self, clause, values) -> bool:
		result = False
		for var in clause:
			value = values[abs(var) - 1] if var > 0 else not values[abs(var) - 1]
			result = result or value
			if result is True: break # if a single term is True, the result will be True regardless of the other terms
		return result

	def binary_counter(self, values: list, idx: list) -> None:
		# Binary addition ripple (+1) step
		for var in idx:
			if values[var] == False:
				values[var] = True
				break
			else:
				values[var] = False

	# basic brute force SAT solver, very inefficient
	def sat_binary(self) -> list:
		values = [False] * self.var_count
		
		while True:
			eval = self.eval_cnf(values)
			
			if eval:
				return values
			if all(values):
				return []

			self.binary_counter(values, list(range(self.var_count)))

	# DPLL algrithm, recursive backtracking, set a variable to True, continue so until a dead end is reached, then rollback changes on by one
	def sat_dpll(self) -> list:
		values = self.dpll([ None ] * self.var_count)
		if values == []:
			return values
		return values
	
	def dpll(self, values: list) -> list:
		while True:
			forced = None # the single variable that must be True to satisfy
			for clause in self.clauses:
				unassigned = []
				satisfied = False
				for var in clause:
					val = values[abs(var) - 1]
					if val is None:
						unassigned.append(var)
					elif val == (var > 0): # if a single is True -> clause already satisfied
						satisfied = True
						break

				if satisfied: continue
				if len(unassigned) == 0: return [] # there are no free vars to set to True -> clause is False, and CNF -> False
				if len(unassigned) == 1:
					forced = unassigned[0]
					break

			if forced is None: break
			values[abs(forced) - 1] = forced > 0

		# pick the first unassigned variable
		var_idx = None
		for i in range(self.var_count):
			if values[i] is None:
				var_idx = i
				break
		# if all assigned SAT
		if var_idx is None:
			return values

		# try both values
		for guess in (True, False):
			branch = values[:]
			branch[var_idx] = guess
			# if evaluates to True - solved
			result = self.dpll(branch)
			if len(result) > 0:
				return result
		# if nor True nor False works - UNSAT
		return []