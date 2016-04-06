

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

# -35.3x^3 + 45x^2 - 3.4x + 0.005

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
						self.coefficients.append(float(term[1:x_index]))
				else:
					
					# Implicit 1
					if len(term[:x_index]) == 0:
						self.coefficients.append(1)
					else:
						self.coefficients.append(float(term[:x_index]))
			
			# Constant
			elif 'x' not in term:
				if '-' in term:
					self.coefficients.append(term[1:])
				else:
					self.coefficients.append(float(term))



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