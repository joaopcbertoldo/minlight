import sys
import time

from hyperopt import hp, Trials, fmin, tpe

from src.simulation.max_tension import configs as cfg


def search_space():
    # x
    X1_x_spaces = []
    for X1 in cfg.Fixation.X1_vals:
        min = cfg.Source.Center.x_min  # min
        max = cfg.Source.Center.x_max(X1)  # max
        x_space = hp.uniform('x_X1_' + str(int(X1)), min, max)  # space

        X1_x_spaces.append((X1, x_space))  # apppend

    # y
    min = cfg.Source.Center.y_min  # min
    max = cfg.Source.Center.y_max  # max
    y_space = hp.uniform('y', min, max)  # space

    # z
    min = cfg.Source.Center.z_min  # min
    max = cfg.Source.Center.z_max  # max
    z_space = hp.uniform('z', min, max)  # space

    # row
    min = cfg.Source.Orientation.row_min  # min
    max = cfg.Source.Orientation.row_max  # max
    row_space = hp.uniform('row', min, max)  # space

    # pitch
    min = cfg.Source.Orientation.pitch_min  # min
    max = cfg.Source.Orientation.pitch_max  # max
    pitch_space = hp.uniform('pitch', min, max)  # space

    # yaw
    min = cfg.Source.Orientation.yaw_min  # min
    max = cfg.Source.Orientation.yaw_max  # max
    yaw_space = hp.uniform('yaw', min, max)  # space

    # sub spaces
    sub_spaces = []

    for X1, x_space in X1_x_spaces:
        # sub search spaces (sss)
        sss = {
            # X1
            'X1': X1,
            # x y z
            'x': x_space, 'y': y_space, 'z': z_space,
            # row pitch yaw
            'row': row_space, 'pitch': pitch_space, 'yaw': yaw_space
        }

        # append
        sub_spaces.append(sss)

    # search space
    ss = hp.choice('X1', sub_spaces)

    return {
            # x y z
            'x': X1_x_spaces[0][1], 'y': y_space, 'z': z_space,
            # row pitch yaw
            'row': row_space, 'pitch': pitch_space, 'yaw': yaw_space
        }
    # return ss


class Objective:

    def collect_attachements(self):
        return self.params

    def __call__(self, params):
        self.params = params
        print('params', params)
        print('from collect', self.collect_attachements())

        return 1


def simulate():
    # print(search_space)

    obj = Objective()

    ss = search_space()
    print(ss)
    time.sleep(1)

    global best, trials

    best = fmin(
        #fn=obj,
        fn=lambda x: 1,
        space=ss,
        algo=tpe.suggest,
        max_evals=cfg.Simulation.max_evals,
        trials=trials,
        rstate=cfg.Simulation.random_state,
        verbose=cfg.Simulation.fmin_verbose,
        allow_trials_fmin=cfg.Simulation.allow_trials
    )


trials = Trials()
best = None


def main():
    simulate()


# main
if __name__ == '__main__':
    # arguments
    args = sys.argv[1:]

    # ma-in call
    main(*args)

