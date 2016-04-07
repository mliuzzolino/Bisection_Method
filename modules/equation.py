import numpy as np
import matplotlib.pyplot as plt
from tools import *

class Equation(object):

	def __init__(self):
		get_equation(self)
		self._construct_function()

		# Attributes to initialize later

		# Domain
		self.a = None
		self.b = None

		# X and Y
		self.X = None
		self.Y = []

		# Possible positive and negative solutions as determined by Descarte's Sign Change Rule
		self.positive_solutions = None
		self.negative_solutions = None

		# Max number of possible solutions == highest degree of polynomial
		self.max_number_solutions = None


	def __repr__(self):
		equation_reconstruct = ''
		for index, _ in enumerate(self.powers):
			if index == 0 and self.signs[0] is '+':
				pass
			elif index == 0 and self.signs[0] is '-':
				equation_reconstruct += str(self.signs[index])
				equation_reconstruct += ""
			else:
				equation_reconstruct += str(self.signs[index])
				equation_reconstruct += " "

			if self.coefficients[index] == 1:
				pass
			else:
				equation_reconstruct += str(self.coefficients[index])

			if self.powers[index] == 1:
				equation_reconstruct += "x"
			elif self.powers[index] == 0:
				equation_reconstruct += ""
			else:
				equation_reconstruct += "x^"
				equation_reconstruct += str(self.powers[index])

			equation_reconstruct += " "

		return ("Equation: {}".format(equation_reconstruct))


	def setup(self, a, b, interval=0.0001):
		# Set bounds
		self.a = a
		self.b = b

		# Generate X based on domain input [a, b] with interval
		self.X = np.arange(a, b, interval)

		# Calculate Y
		self.calculate_Y()

		# Determine possible real solutions
		self.possible_real_solutions()

		# Determine maximum number real solutions
		self._calculate_max_number_solutions()


	def calculate_Y(self):
		
		for x in self.X:
			y_value = 0
			for index, power in enumerate(self.powers):
				sign = np.where(self.signs[index] == '+', 1, -1)
				coefficient = sign * self.coefficients[index]
				x_power = x ** power
				term = coefficient * x_power
				y_value += term

			self.Y.append(y_value)


	def sign_switch_count(self, signs):
		solutions_counter = 0
		for index, sign in enumerate(signs):
			if index == 0:
				prev_sign = sign
			if sign is not prev_sign:
				solutions_counter += 1
			prev_sign = sign

		possible_solutions = []
		
		while solutions_counter >= 0:
			possible_solutions.append(solutions_counter)
			solutions_counter -= 2

		return possible_solutions


	def possible_real_solutions(self):
		# Possible positive solutions
		self.positive_solutions = self.sign_switch_count(self.signs)

		# Possible negative solutions
	
		# Determine signs for f(-x)
		neg_signs = []
		for index, power in enumerate(self.powers):
			# Even powers: sign stays the same
			if power % 2 == 0:
				neg_signs.append(self.signs[index])
			# Odd power: flip sign
			else:
				if self.signs[index] is '+':
					neg_signs.append('-')
				elif self.signs[index] is '-':
					neg_signs.append('+')

		self.negative_solutions = self.sign_switch_count(neg_signs)


	def _calculate_max_number_solutions(self):
		self.max_number_solutions = max(self.powers)


	def _construct_function(self):

		# Capture signs, powers, and coefficients of terms
		capture_signs(self)
		capture_powers(self)
		capture_coefficients(self)

		#print_reconstructed_equation(signs, coefficients, powers)

		self.equation = {}
		for index, power in enumerate(self.powers):
			value = [self.signs[index], self.coefficients[index]]
			self.equation[power] = value


	def plot(self, roots = None):
		plt.plot(self.X, self.Y, color='blue')

		if roots:
			plt.plot(self.X, np.zeros(len(self.Y)), 'r--')

			for root_x, root_y in roots.values():
				print("Root at {:.2f}".format(root_x))
				plt.plot(root_x, root_y, 'ro')
				plt.plot(np.ones(len(self.X)) * root_x, self.Y, 'b--')
			

		plt.axis([min(self.X)-max(self.X)*0.25, max(self.X)+max(self.X)*0.25, min(self.Y)-max(self.Y)*0.25, max(self.Y)+max(self.Y)*0.25])
		plt.show()
