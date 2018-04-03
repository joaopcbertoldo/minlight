import sys
from src.simulation.max_tension.main import main


# main
if __name__ == '__main__':
    # arguments
    args = sys.argv[1:]

    # main call
    main(*args)
