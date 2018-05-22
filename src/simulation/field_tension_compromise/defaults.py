# imports
import numpy as np


class Constants:

    # 0.1.8.1 - max, min and n values for the latitude of an observer on earth
    MIN_LATITUDE = -90.0
    MAX_LATITUDE = 90.0
    MIN_N_LATITUDE = 1

    # 0.1.8.2 - max, min and n values for orientation of the sun from an observer's pov
    MIN_ORIENTATION = 0.0
    MAX_ORIENTATION = 180.0
    MIN_N_ORIENTATION = 1

    # 0.1.8.3 - #points in each trajectory (min and max)
    MIN_N_POINTS_TRAJECTORY = 2
    MAX_N_POINTS_TRAJECTORY = np.inf

    # 0.1.8.4 - days of the year id numbers (firts and last)
    FIRST_DAY_YEAR = 1
    LAST_DAY_YEAR = 365

