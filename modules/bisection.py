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
		self.positive_domains = [(a_i-5, b_i)]

		a_i = 0
		b_zero = np.where(np.abs(self.X) < 1e-10)
		b_i = list(b_zero)[0][0]
		self.negative_domains = [(a_i, b_i+5)]

		# 
		self.x_ns = None

		self.num_real_pos_solutions = equation.positive_solutions
		self.num_real_pos_solutions.pop(-1)
		self.num_real_neg_solutions = equation.negative_solutions
		self.num_real_neg_solutions.pop(-1)
		self.max_iterations = 1e5
		self.tolerance = 0.001

		self.roots = {}


	def duplicate_root(self):

		for key in self.roots.keys():
			# Found duplicate
			if np.abs(self.x_ns - key) < 10:
				return True

		# Didn't find duplicate
		return False

	def run_bisection_method(self, a_i, b_i):
		Y_a = self.Y[a_i]
		Y_b = self.Y[b_i]
		root_found = False
		
		#if Y_a * Y_b > 0:
		while Y_a * Y_b > 0:
			a_i += 1
			Y_a = self.Y[a_i]
		

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
				if not self.duplicate_root():
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
		#print("Max possible real roots: {}".format(self.max_roots))
		
		# Check possible positive roots
		while self.num_real_pos_solutions:
			print("Possible positive reals: {}".format(self.num_real_pos_solutions))
			# Check if odd or even. Odd -> at least 1 solution exists
			value = '+'
			self.find_roots(self.positive_domains, value)
			print(self.roots)
			print
				

		
		# Check possible negative roots
		while self.num_real_neg_solutions:
			print("Possible negative reals: {}".format(self.num_real_neg_solutions))
			# Check if odd or even. Odd -> at least 1 solution exists
			value = '-'
			self.find_roots(self.negative_domains, value)
			print(self.roots)
			print

		self.equation.plot(self.roots)



	def update_num_real_solutions(self, possible_solutions, adjust_factor):
		print("Updating possible solutions: {}".format(possible_solutions))

		new_num_real_solutions = []
		for num in possible_solutions:
			new_num = num - adjust_factor
			if new_num > 0:
				new_num_real_solutions.append(new_num)
		
		return new_num_real_solutions[:]
		


	def update_domains(self, domains):
		new_domains = []

		for domain in domains:
			A_i = domain[0]
			B_i = domain[1]

			if self.x_ns > A_i and self.x_ns < B_i:
				new_domains.append((A_i, self.x_ns))
				new_domains.append((self.x_ns, B_i))

			else:
				new_domains.append((A_i, B_i))

		return new_domains[:]
		


	def find_roots(self, domains, value):
		if value == '+':
			possible_solutions = self.num_real_pos_solutions
		elif value == '-':
			possible_solutions = self.num_real_neg_solutions

		print("Possible {} solutions: {}".format(value, possible_solutions))

		if len(possible_solutions) == 0:
			return

		# Odd case
		elif possible_solutions[0] % 2 != 0:
			print("Odd!")

			# Check for solution in each domain
			print("Domains: {}".format(domains))
			for domain in domains:
				print("domain: {}".format(domain))
				a_i = domain[0]
				b_i = domain[1]
				print("a_i: {}".format(a_i))
				print("b_i: {}".format(b_i))

				# If run_bisection_method returns True, root was found!
				if self.run_bisection_method(a_i, b_i):
					print("Root found! {}".format(self.X[self.x_ns]))

					# If roots not populated yet, add this root
					if len(self.roots.keys()) == 0:
						print("Instantiating Root Dictionary! {} added".format(self.x_ns))
						self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])

					# Else, check to see if the root already exists in root dictionary
					else:
						duplicate_root = False
						for key in self.roots.keys():
							if np.abs(self.x_ns - key) < 10:
								duplicate_root = True
								
						if not duplicate_root:
							self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])

				# Update possible_solutions
				possible_solutions = self.update_num_real_solutions(possible_solutions, 1)
				print("Updated possible solutions: {}".format(possible_solutions))

				# Update domains
				domains = self.update_domains(domains)


	

		# Even case!
		else:
			print("Even!")
			print("Domains: {}".format(domains))
			for domain in domains:
				print("domain: {}".format(domain))
				a_i = domain[0]
				b_i = domain[1]
				print("a_i: {}".format(a_i))
				print("b_i: {}".format(b_i))
				# Look for root
				# If root exists
				if self.run_bisection_method(a_i, b_i):
					print("Root found! {}".format(self.X[self.x_ns]))

					# Checks if root dictionary is empty. 
					if len(self.roots.keys()) == 0:
						self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])
					# Else, determines if root already exists in dictionary
					else:
						duplicate_root = False
						for key in self.roots.keys():
							if np.abs(self.x_ns - key) < 10:
								duplicate_root = True
															
						if not duplicate_root:
							self.roots[self.x_ns] = (self.X[self.x_ns], self.Y[self.x_ns])

					# Update possible_solutions
					possible_solutions = self.update_num_real_solutions(possible_solutions, 1)
					print("Updated possible solutions: {}".format(possible_solutions))
		
					
					## Update domains
					domains = self.update_domains(domains)
					print("Domains: {}".format(domains))

			# else root doesn't exist
			
			# Update possible_solutions
			possible_solutions = self.update_num_real_solutions(possible_solutions, 2)
			print("Updated possible solutions: {}".format(possible_solutions))
					

		if value == '+':
			self.num_real_pos_solutions = possible_solutions[:]
		elif value == '-':
			self.num_real_neg_solutions = possible_solutions[:]
		# Recursion!
		self.find_roots(domains, value)
