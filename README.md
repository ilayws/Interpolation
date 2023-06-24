# Interpolation

Takes a series of points and interpolates their graph with one of two methods:
1. Creating a bezier curve out of the n points
2. Find the polynomial that goes through the n points by create a system of equations, expressing them in matrix form, reducing to echilon form with gaussian elimination, then calculating the polynomial's coefficients. This method works very well for n<11
