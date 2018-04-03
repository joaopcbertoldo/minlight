
# ! everythin in mm ! ! everythin in mm ! ! everythin in mm ! ! everythin in mm ! ! everythin in mm !

"""
cables' fixations' positions (from Chloé)
point de référence : haut de la poulie, d'où part le câble

fixation	  x     y	    z
000	        1950	325	    400
001	        1950	325	    3750
010	        1950	4675	400
011	        1950	4675	3750
100	        5000	325	    400
101	        5000	325	    3750
110	        5000	4675	400
111	        5000	4675	3750

TODO doc this notation
Notation used here:
    X0 refers to the X's value for points where fixation is 0YZ
    X1 refers to the X's value for points where fixation is 1YZ
    Y0 idem...
    Y1 idem...
    Z0 idem...
    Z1 idem...

    cf the notation for box vertices

    !!!! these are the fixation points --> they define the limits of the grids

    n = number of discretization
"""

# range for X0 - it won't change at first
X0_min = 1950.
X0_max = 1950.
X0_n = 1

# X0 =

# range for X1 - this is the mobile part (close to the maisonette)
X1_min = 5000.
X1_max = 10000.
X1_n = 3

# X1 =

# Y0 and Y1 fixed
Y0 = 325.
Y1 = 4675.

# Z0 and Z1 fixed
Z0 = 400.
Z1 = 3750.








