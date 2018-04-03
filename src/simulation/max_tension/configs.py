import numpy as np

from src.setups import palaiseau
from src.enums import AngleUnityEnum
from src.toolbox.useful import get_terminal_size


# setup
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


class Simulation:

    max_evals = 10
    random_state_fixed = True
    allow_trials = False

    fmin_verbose = 0
    script_verbose = 0
    config_verbose = 1

    @staticmethod
    def random_state():
        return 42 if Simulation.random_state_fixed else np.randint(1, 1000)


class Fixation:

    # fix_X0 - it won't change at first
    X0 = 1950.

    # range for X1 - this is the mobile part (close to the maisonette)
    X1_min = 5000.
    X1_max = 10000.
    X1_n = 2

    X1_vals = np.linspace(X1_min, X1_max, X1_n)

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

    class Orientation:
        # angles unity
        angles_unity = AngleUnityEnum.degree

        # row min
        row_min = 0

        # row max
        row_max = 0

        # pitch min
        pitch_min = -45

        # pitch max
        pitch_max = +45

        # yaw min
        yaw_min = -90

        # yaw max
        yaw_max = +90


(width, height) = get_terminal_size()


def print_separator(msg: str = None):
    msg = ' ' + str(msg) + ' ' if msg else ''
    msg = msg.center(width, '-')
    print(msg)


def config_verbose_1():
    print('setup: ', stp.__name__)
    print_separator('source')
    print('source length: ', stp.Source.Dimensions.length)
    print('source width: ', stp.Source.Dimensions.width)
    print('source height: ', stp.Source.Dimensions.height)
    print_separator('fixation')
    print('X0', Fixation.X0)
    print('X1 values: ', list(f'{val:.0f}' for val in Fixation.X1_vals))
    print('Y0', Fixation.Y0)
    print('Y1', Fixation.Y1)
    print('Z0', Fixation.Z0)
    print('Z1', Fixation.Z1)


def verbose():
    print_separator()
    print_separator('CONFIG VERBOSE')

    if Simulation.config_verbose == 0:
        pass
    elif Simulation.config_verbose == 1:
        config_verbose_1()
    else:
        print('INVALID CONFIG VERBOSE VALUE')

    print_separator()
    print_separator()
    print()
    print()

verbose()
