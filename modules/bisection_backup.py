from __future__ import division
import numpy as np

class Bisection(object):

	def __init__(self, equation):
		self.equation = equation
		self.max_roots = equation.max_number_solutions

		self.X = equation.X
		self.Y = equation.Y

		# Setup initial domains for pos and neg
		a_zero = np.where(np.abs(self.X) < 1e-10)
		a_i = int(list(a_zero)[0][0])
		b_i = len(self.X) - 1
		self.positive_domains = [(a_i, b_i)]

		a_i = 0
		b_zero = np.where(np.abs(self.X) < 1e-10)
		b_i = list(b_zero)[0][0]
		self.negative_domains = [(a_i, b_i)]

		# 
		self.x_ns = None

		self.num_real_pos_solutions = equation.positive_solutions
		self.num_real_neg_solutions = equation.negative_solutions

		self.max_iterations = 1e5
		self.tolerance = 0.001

		self.roots = {}


	def run_method(self, a_i, b_i):
		# Initialize x_numerical_solution and it's corresponding f_ns
		x_ns = (a_i + b_i) // 2
		f_ns = self.Y[x_ns]



		n = 0
		while n < self.max_iterations:
			f_ns_prev = f_ns

			# Find new midpoint index, x_ns, and its y value
			x_ns = (a_i + b_i) // 2
			f_ns = self.Y[x_ns]
	
			# Check if solution found within tolerance
			if np.abs(0 - f_ns) < self.tolerance:

				break

			# Determine new bounds
			if self.Y[a_i] * f_ns > 0:
				a_i = x_ns
			else:
				b_i = x_ns
			
			n += 1

		else:
			return False

		self.x_ns = x_ns
		return True


	def run(self):
		print("Max possible real roots: {}".format(self.max_roots))
		
		


		# Check possible positive roots	
		"""
			Examples of list:
				[5, 3, 1]		->		5 possible solutions in positive domain
										However, at least 1 real solution must exist

				Check for known real solution, c1, in [0, b]

				Once found, set domains: [0, c1), (c1, b].

				4 possible solutions remain: [5, 3, 1] -> [4, 2, 0]

				Could be 2 sets of imaginary solutions...
				Check [0, c1) and (c1, b] for solutions.
				if no solutions, 
					c1 is only solution; other 4 are imaginary.
				else solution exists
					if c2 in [0, c1) or c2 in (c1, b]
						set domains: [0, c2), (c2, c1) or (c1, c2), (c2, b]
					[4, 2, 0] -> [3, 1]

				3 possible solutions remain; at least 1 more real solution exists

				check [0, c2), (c2, c1) or (c1, c2), (c2, b] for solution
				once c3 found, set domains as
					1. [0, c3), (c3, c2), (c2, c1)
					2. [0, c2), (c2, c3), (c3, c1)]
					3. (c1, c3), (c3, c2), (c2, b]
					4. (c1, c2), (c2, c3), (c3, b]

				[3, 1] -> [2, 0]
				2 possible solutions. They could be an imaginary pair of roots
				if no solution,
					[2, 0] -> [0]
				else:
					update domains
					[2, 0] -> [1]

				1 solution remains. find it in remaining intervals

		"""
		while self.num_real_pos_solutions:
			print("Possible pos reals: {}".format(self.num_real_pos_solutions))
			value = 'positive'
			# Check if odd or even. Odd -> at least 1 solution exists
			self.find_roots(self.num_real_pos_solutions, value)
			print(self.roots)
				

		
		# Check possible negative roots
		while self.num_real_neg_solutions:
			print("Possible neg reals: {}".format(self.num_real_neg_solutions))
			value = 'negative'
			# Check if odd or even. Odd -> at least 1 solution exists
			self.find_roots(self.num_real_neg_solutions, value)
			print(self.roots)

		self.equation.plot(self.roots)



	def update_num_real_solutions(self, possible_solutions, adjust_factor, value):

		new_num_real_solutions = []
		for num in possible_solutions:
			new_num = num - adjust_factor
			if new_num >= 0:
				new_num_real_solutions.append(new_num)
		if value == 'positive':
			self.num_real_pos_solutions = new_num_real_solutions[:]
		elif value == 'negative':
			self.num_real_neg_solutions = new_num_real_solutions[:]
	

	def update_domains(self, value):
		new_domains = []
		if value == 'positive':
			old_domain = self.positive_domains[:]
		elif value == 'negative':
			old_domain = self.negative_domains[:]
		for domain in old_domain:
			A_i = domain[0]
			B_i = domain[1]

			if self.x_ns > A_i and self.x_ns < B_i:
				new_domains.append((A_i, self.x_ns))
				new_domains.append((self.x_ns, B_i))

			else:
				new_domains.append((A_i, B_i))

		if value == 'positive':
			self.positive_domains = new_domains[:]
		elif value == 'negative':
			self.negative_domains = new_domains[:]
		



	def find_roots(self, possible_solutions, value):

		if len(possible_solutions) == 0:
			return

		# Odd case
		elif possible_solutions[0] % 2 != 0:
			print("Odd!")
			if value == 'positive':
				old_domain = self.positive_domains
			elif value == 'negative':
				old_domain = self.negative_domains

			for domain in old_domain:
				a_i = domain[0]
				b_i = domain[1]

				if self.run_method(a_i, b_i):
					if len(self.roots.keys()) == 0:
						self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])
					else:
						duplicate_root = False
						for key in self.roots.keys():
							if np.abs(self.x_ns - key) < 10:
								duplicate_root = True
								
						if not duplicate_root:
							self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])

				# Update possible_solutions
				self.update_num_real_solutions(possible_solutions, 1, value)

				# Update domains
				self.update_domains(value)
	

		# Even case!
		else:
			print("Even!")
			if value == 'positive':
				old_domain = self.positive_domains
			elif value == 'negative':
				old_domain = self.negative_domains
				
			for domain in old_domain:
				a_i = domain[0]
				b_i = domain[1]

				# Look for root
				# root exists
				if self.run_method(a_i, b_i):
					if len(self.roots.keys()) == 0:
						self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])
					else:
						duplicate_root = False
						for key in self.roots.keys():
							if np.abs(self.x_ns - key) < 10:
								duplicate_root = True
															
						if not duplicate_root:
							self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])

					# Update possible_solutions
					self.update_num_real_solutions(possible_solutions, 1, value)
					
					## Update domains
					self.update_domains(value)

				# root doesn't exist
				else:
					# Update possible_solutions
					self.update_num_real_solutions(possible_solutions, 2, value)


		# Recursion!
		self.find_roots(possible_solutions, value)
