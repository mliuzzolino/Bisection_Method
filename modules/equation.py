import numpy as np
import matplotlib.pyplot as plt

class Equation(object):

	def __init__(self):
		self.get_equation()
		self.construct_function()

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


	def setup(self, a, b, interval=0.0001):
		# Set bounds
		self.a = a
		self.b = b

		# Calculate X
		self.X = np.arange(a, b, interval)

		# Calculate Y
		self.calculate_Y()

		# Determine possible real solutions
		self.possible_real_solutions()

		# Determine maximum number real solutions
		self.calculate_max_number_solutions()


	def calculate_Y(self):
		
		for x in self.X:
			y_value = 0
			for index, power in enumerate(self.powers):
				sign = np.where(self.signs[index] == '+', 1, -1)
				coefficient = sign * int(self.coefficients[index])
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
			if int(power) % 2 == 0:
				neg_signs.append(self.signs[index])
			# Odd power: flip sign
			else:
				if self.signs[index] is '+':
					neg_signs.append('-')
				elif self.signs[index] is '-':
					neg_signs.append('+')

		self.negative_solutions = self.sign_switch_count(neg_signs)


	def calculate_max_number_solutions(self):
		self.max_number_solutions = max(self.powers)


	def get_equation(self):
		print("\n")
		print("\tPlease enter a polynomial")
		print("\tE.g., x^3 - 3x^2 + 3\n")
		user_function = raw_input(">> ")

		print("\nEquation: {}\n\n".format(user_function))

		self.raw_equation = user_function.split(' ')



	def capture_signs(self):
		self.signs = []
		for index, term in enumerate(self.raw_equation):
			# Capture signs
			if index == 0 and term[0] is not '-':
				self.signs.append('+')

			elif index == 0 and term[0] is '-':
				self.signs.append('-')

			elif index % 2 != 0:
				self.signs.append(term)	



	def capture_coefficients(self):
		self.coefficients = []
		for index, term in enumerate(self.raw_equation):

			# Only looks at even-numbered terms. (odd numbered terms are signs)
			if index % 2 == 0:

				if 'x' in term:
					x_index = term.index('x')
					if '-' in term:
						# Implicit 1
						if len(term[1:x_index]) == 0:
							self.coefficients.append(1)
						else:
							self.coefficients.append(term[1:x_index])
					else:
						# Implicit 1
						if len(term[:x_index]) == 0:
							self.coefficients.append(1)
						else:
							self.coefficients.append(term[:x_index])
				
				# Constant
				elif 'x' not in term:
					if '-' in term:
						self.coefficients.append(term[1:])
					else:
						self.coefficients.append(int(term))	


	def capture_powers(self):
		self.powers = []
		for index, term in enumerate(self.raw_equation):
			if index % 2 == 0:
				if 'x^' in term:
					index = term.index('^') + 1
					self.powers.append(int(term[index:]))
				elif 'x' in term:
					self.powers.append(1)
				elif 'x' not in term:
					self.powers.append(0)


	def construct_function(self):

		# Capture signs of terms
		self.capture_signs()
		
		# Capture powers of terms
		self.capture_powers()

		# Capture coefficients
		self.capture_coefficients()

		#print_reconstructed_equation(signs, coefficients, powers)

		self.equation = {}
		for index, power in enumerate(self.powers):
			value = [self.signs[index], self.coefficients[index]]
			self.equation[power] = value


	def __repr__(self):
		equation_reconstruct = ''
		for index, _ in enumerate(self.powers):
			if index == 0 and self.signs[0] is '+':
				pass
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


	def plot(self, roots = None):
		plt.plot(self.X, self.Y, color='blue')

		if roots:
			plt.plot(self.X, np.zeros(len(self.Y)), 'r--')

			for root_x, root_y in roots:
				print("Root at {}".format(root_x))
				plt.plot(root_x, root_y, 'ro')
				plt.plot(np.ones(len(self.X)) * root_x, self.Y, 'b--')
			

		plt.axis([min(self.X)-max(self.X)*0.25, max(self.X)+max(self.X)*0.25, min(self.Y)-max(self.Y)*0.25, max(self.Y)+max(self.Y)*0.25])
		plt.show()
