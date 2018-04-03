import numpy as np
from src.setups import palaiseau

stp = palaiseau

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
    fix_X0 refers to the X's value for points where fixation is 0YZ
    X1 refers to the X's value for points where fixation is 1YZ
    fix_Y0 idem...
    Y1 idem...
    Z0 idem...
    Z1 idem...

    cf the notation for box vertices

    !!!! these are the fixation points --> they define the limits of the grids

    n = number of discretization
"""


class Fixation:

    # fix_X0 - it won't change at first
    X0 = 1950.

    # range for X1 - this is the mobile part (close to the maisonette)
    X1_min = 5000.
    X1_max = 10000.
    X1_n = 3

    X1_range = np.linspace(X1_min, X1_max, X1_n)

    # fix_Y0 and Y1 fixed
    Y0 = 325.
    Y1 = 4675.

    # Z0 and Z1 fixed
    Z0 = 400.
    Z1 = 3300.


class Source:

    class Center:
        # x min
        x_min = Fixation.X0 + stp.Source.Dimensions.length / 2

        # x max = f(X1)
        @staticmethod
        def x_max(X1):
            return X1 - stp.Source.Dimensions.length / 2

        # y min
        y_min = Fixation.Y0 + stp.Source.Dimensions.width / 2

        # y max
        y_max = Fixation.Y1 - stp.Source.Dimensions.width / 2

        # z min
        z_min = Fixation.Z0 + stp.Source.Dimensions.height / 2

        # z max
        z_max = Fixation.Z1 - stp.Source.Dimensions.height / 2

        # n of discretization
        x_n = 5
        y_n = 5
        z_n = 5

    class Orientation:
        pass





