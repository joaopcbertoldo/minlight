
# imports
import sys
import os
import re

# this directory
thisdir = os.path.abspath('.')

# project's parent directory
parentdir = re.sub(r'minlight.*', 'minlight', thisdir)

# insert it tho the path
sys.path.insert(0, parentdir)


# project imports
from src.simulation.field_tension_compromise.parsing._valid_types import \
    valid_max, valid_min, valid_n_discretisation, valid_borned_int, valid_borned_float, valid_alias


# add a set of three paremeters to specify a discretized real field (min, max, n), n for the #values
def add_discretized_real_field(parser, name: str, min: float, max: float, min_n: int):
    # min - help msg
    help_ = f"Minimal value of {name}. Format float >= {min}."

    # min
    parser.add_argument('min_' + name, type=valid_min(name, float, min), help=help_)

    # max - help msg
    help_ = f"Maximal value of {name}. Format float >= {max}."

    # max
    parser.add_argument('max_' + name, type=valid_max(name, float, max), help=help_)

    # n - help msg
    help_ = f"Number of {name} values (from {'min_' + name} to {'max_' + name}). "
    help_ += f"Format: integer >= {min_n}."

    # n
    parser.add_argument('n_' + name, type=valid_n_discretisation(name, min_n), help=help_)


# add a borned integer
def add_borned_int_argument(parser, name: str, min: int, max: int):
    # help msg
    help_ = f"{name} is an integer from '{min}' to '{max}'. "

    # add argument
    parser.add_argument(name, type=valid_borned_int(name, min, max), help=help_)


# add a list of borned integers
def add_borned_int_list_argument(parser, name: str, min: int, max: int):
    # help msg
    help_ = f"(list of values) All values of '{name}' must be integers from '{min}' to '{max}'. "

    assert name[0:2] == '--', "A list argument's name must begin with '--'."

    # add argument
    parser.add_argument(name, nargs='+', type=valid_borned_int(name, min, max), help=help_)


# add a borned integer
def add_borned_float_argument(parser, name: str, min: int, max: int):
    # help msg
    help_ = f"{name} is a float from '{min}' to '{max}'. "

    # add argument
    parser.add_argument(name, type=valid_borned_float(name, min, max), help=help_)


def add_debug(parser, propagate_to_subparsers: bool = True):
    pass


def add_alias_argument(parser):
    # help msg
    help_ = f"The alias is like a nickname for the set of parameters. " \
            f"It is also used to identify the file that has those parameters."

    # add argument
    parser.add_argument('alias', type=valid_alias, help=help_)


# from the create_paremeter_subparsers, create the respective show_paremeter_subparsers
def add_show_parameter_parsers(create_paremeter_subparsers, show_paremeter_subparsers):

    # repeat for each parameter name
    for parameter in create_paremeter_subparsers.choices:

        # parser help msg
        help_ = f"Show parameter files for {parameter}. " \
                f"If alias is given -> show respective file's content. " \
                f"Otherwise -> show all aliases available."

        # add the parser
        parser = show_paremeter_subparsers.add_parser(parameter, description=help_, help=help_)

        # alias help msg
        help_ = "Alias of particular paremeter file to be shown."

        # add alias argument
        parser.add_argument('-a', '--alias', type=str, help=help_)
