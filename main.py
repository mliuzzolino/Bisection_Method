import numpy as np
from modules.equation import Equation
from modules.bisection import Bisection


def main():
	user_continue = True

	while user_continue:

		eq = Equation()
		eq.setup(-8, 8)
		
		bisection = Bisection(eq)
		bisection.run()

		user_continue = np.where(raw_input("Continue (y/n)? ") == 'y', True, False)
		

if __name__ == '__main__':
	main()