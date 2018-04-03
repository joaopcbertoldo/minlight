import hyperopt as hopt
from hyperopt import hp
from src.simulation.max_tension import configs as cfg
import sys



X1_x_grids = []
for X1 in cfg.fix_X1_range:
    # x
    grid_x = hp.uniform('x', cfg.fix_X0, X1)


    # z
    grid_z =
    X1_grids.append((X1, ))

# y_min
grid_y = hp.quniform('y', cfg.Source.Center.y_min, cfg.Source.Center.y_max, )


def main(*args):
    pass


# main
if __name__ == '__main__':
    # arguments
    args = sys.argv[1:]

    # main call
    main(*args)

