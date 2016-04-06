# Bisection Method

## Introduction
This script uses the bisection method to find the roots of polynomials. Descartes' Sign Rule is utilized to determine the maximum possible number of real solutions, delineated into the number of possible positive real roots and negative real roots. The algorithm then searches the positive domain for roots until the possible positive real roots number is depleated. Similarly, the negative domain is searched for roots.

## Run
From the parent folder, run:

    >>> python main.py

## Input Format
Polynomial coefficients may take on any real value. Powers must be represented with the carot, ^, and a space must be placed between each term and "+" or "-". Do not use '*' to represent multiplication; e.g., 3 * x is incorrect. Rather, just input 3x.

For example, the following is acceptable:

    >> 3x^3 - 0.5x^2 - 5x + 50.0
  
However, the following will result in error:

    >> 3x^3 -x^2 - 5x+ 50

## Issues
### Input
The input format needs to be made more flexible such that spaces aren't an issue. The function input should be expanded to include functions other than polynomials.

### Root Finding
Tolerances and max_iterations need to be checked for appropriateness. The algorithm for checking the positive and negative possible real root domains needs to be adjusted. For instance, I believe that if two real roots exist within the positive domain, the same one will be found twice. Thus, the algorithm needs to be altered such that once it finds the first root, it changes the initial lower and upper boundaries of the search domain such that it will be able to find the unique root.

### Code Cleanup
The coding and algorithms need to be optimized. This was my first-pass attempt at writing the bisection method, and there is pleanty of room for improvement amongst all elements of the script. 
