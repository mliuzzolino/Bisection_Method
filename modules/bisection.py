from __future__ import division
import numpy as np

class Bisection(object):

	def __init__(self, equation):
		self.equation = equation
		self.max_roots = equation.max_number_solutions

		self.X = equation.X
		self.Y = equation.Y

		self.a_i = None
		self.b_i = None

		self.x_ns = None

		self.num_real_pos_solutions = equation.positive_solutions
		self.num_real_neg_solutions = equation.negative_solutions

		self.max_iterations = 1e5
		self.tolerance = 0.001

		self.roots = []


	def run_method(self):
		# Initialize x_numerical_solution and it's corresponding f_ns
		x_ns = (self.a_i + self.b_i) // 2
		f_ns = self.Y[x_ns]

		n = 0
		while n < self.max_iterations:
			f_ns_prev = f_ns

			# Find new midpoint index, x_ns, and its y value
			x_ns = (self.a_i + self.b_i) // 2
			f_ns = self.Y[x_ns]
	
			# Check if solution found within tolerance
			if np.abs(0 - f_ns) < self.tolerance:

				break

			# Determine new bounds
			if self.Y[self.a_i] * f_ns > 0:
				self.a_i = x_ns
			else:
				self.b_i = x_ns
			
			n += 1

		else:
			return False

		self.x_ns = x_ns
		return True


	def run(self):

		# Checks trivial case of 1 solution at x = 0
		if self.num_real_pos_solutions[0] == 0 and self.num_real_neg_solutions[0] == 0:
			self.roots = [(0, 0)]
			self.equation.plot(self.roots)
			return

		

		# Check Positive roots
		if len(self.num_real_pos_solutions) == 1:
			# 1 real positive root exists
			a = np.where(np.abs(self.equation.X) < 1e-10)
			self.a_i = int(list(a)[0][0])
			self.b_i = len(self.X) - 1

			if self.run_method():
				self.roots.append((self.X[self.x_ns], self.Y[self.x_ns]))
			
			self.max_roots -= 1			


		# Check Negative roots

		if len(self.num_real_neg_solutions) == 1:
			# 1 real negitive root exists
			self.a_i = 0
			b = np.where(np.abs(self.equation.X) < 1e-10)
			self.b_i = list(b)[0][0]

			if self.run_method():
				self.roots.append((self.X[self.x_ns], self.Y[self.x_ns]))
			
			self.max_roots -= 1	


		self.equation.plot(self.roots)


		

	
