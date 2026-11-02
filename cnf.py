from sys import stdout
from tqdm import tqdm

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

	def sat_binary(self) -> list:
		values = [False] * self.var_count

		with tqdm(total=2 ** self.var_count) as pbar:
			while True:
				eval = self.eval_cnf(values)
				
				if eval:
					return values
				if all(values):
					return []

				self.binary_counter(values, list(range(self.var_count)))
				
				pbar.update(1)

	def sat_calculate(self) -> list:
		values_final = [False] * self.var_count
		values_set = [False] * self.var_count

		with tqdm(total=2 ** self.var_count) as pbar:
			for clause in self.clauses:
				for var in clause:
					var_idx = abs(var) - 1
					if all(values_set) is True:
						return values_final
					# don't modify a set value
					if values_set[var_idx] is True: continue
					# set one variable to eval this clause to True
					if var > 0: values_final[var_idx] = True
					else: values_final[var_idx] = False

					# find all clauses containing the var
					tmp_clauses = [_ for _ in self.clauses if (var in _ or -var in _ )]
					for tmp_clause in tmp_clauses:
						# if one of the clauses evals to False, degrades the whole cnf - so if SAT is to be achieved this var MUST have NOT value 
						if self.eval_clause(tmp_clause, values_final) is False:
							values_final[var_idx] = not values_final[var_idx]
							values_set[var_idx] = True
							print(var, values_final[var_idx])
							break
					pbar.update(1)
			unresolved_vars = [idx for idx in range(self.var_count) if values_set[idx] is False]
			# unresolved_values = [ False ] * len(unresolved_vars)

			# print(unresolved_values)

			limit = 2 ** len(unresolved_vars)
			counter = 0

			while True:
				eval = self.eval_cnf(values_final)
				
				if eval:
					return values_final
				if counter >= limit:
					return []
				self.binary_counter(values_final, unresolved_vars)
				counter += 1
			
			print(values_set)
			print(values_final)
			return []

		# for clause in self.clauses:
		# 	for var in clause:
		# 		# all clauses containing the var
		# 		tmp_clauses = [_ for _ in self.clauses if (var in _ or -var in _ )]
		# 		flat = [abs(_) for clause in tmp_clauses for _ in clause]
		# 		tmp_vars = list(set(flat))
		# 		tmp_vars.remove(abs(var))
		# 		# print(tmp_vars)
		# 		tmp_vars = [ var_pass for var_pass in tmp_vars if values_set[var_pass - 1] is True]

		# 		values = [ val for val in values_final ]
		# 		values_true = [0] * self.var_count
		# 		values_false = [0] * self.var_count

		# 		for tmp_clause in tmp_clauses:
		# 			if self.eval_clause(tmp_clause, values):
		# 				values_true[abs(var) - 1] += 1
		# 			else:
		# 				values_false[abs(var) - 1] += 1

		# 			self.binary_counter(values, list(tmp_vars))
		# 		if values_true[abs(var) - 1] >= values_false[abs(var) - 1]:
		# 			values_final[abs(var) - 1] = True
		# 		else:
		# 			values_final[abs(var) - 1] = False
		# 		values_set[abs(var) - 1] = True
		# 	if all(values_set):
		# 		return values_final
		return []
