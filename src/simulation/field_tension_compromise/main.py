# -*- coding: utf-8 -*-
"""
Main.
"""

import sys
import os
import argparse
import re

# this directory
thisdir = os.path.abspath('.')

# project's parent directory
parentdir = re.sub(r'minlight.*', 'minlight', thisdir)

# insert it tho the path
sys.path.insert(0, parentdir)

# project imports
from src.simulation.field_tension_compromise import defaults as dft


# ----------------------------------------------- main_parser ----------------------------------------------------------
# construction of the main_parser

# the main main_parser (which holds several parsers for the commands)
main_parser = argparse.ArgumentParser(prog='field_tension_compromise',
                                      description='description of prog')

# debug option
main_parser.add_argument('--debug', action='store_true', help='Show debug messages.')

# main_subparsers (the commands)
main_subparsers = main_parser.add_subparsers(metavar='command', help='Command to execute.', dest='command')

# create_parameter_parser
desc = 'Create a parameter file for some part of the workflow.'
create_parameter_parser = main_subparsers.add_parser('create_parameter', description=desc, help=desc)

# show_parameter_parser
desc = 'Show the available parameter files or their contents.'
show_parameter_parser = main_subparsers.add_parser('show_parameter', description=desc, help=desc)

# -------------------------------------------- create_parameter_parser -------------------------------------------------
# construction of the create_parameter_parser

# debug option
create_parameter_parser.add_argument('--debug', action='store_true', help='Show debug messages.')

# create_paremeter_subparsers (the different parameters groups)
create_paremeter_subparsers = create_parameter_parser.add_subparsers(metavar='parameter', help='Parameter to create.',
                                                                     dest='parameter')

# spherical's parser (spherical reference system)
desc = "Create a spherical reference system for the window (position and orientation)."
spherical_parser = create_paremeter_subparsers.add_parser('spherical', description=desc, help=desc)

# rho_roll_liberty's parser
# (range where rho and roll can vary to search feasible positions)
desc = "Create a rho and roll liberty field (2D range to search possible positions)."
rho_roll_liberty_parser = create_paremeter_subparsers.add_parser('rho_roll_liberty', description=desc, help=desc)

# fixation's parser (fixation's positions to test)
desc = "Create a set of fixation positions to test."
fixation_parser = create_paremeter_subparsers.add_parser('fixation', description=desc, help=desc)

# cable_layout's parser (set of cable layouts to test)
desc = "Create a set of cable layouts to test."
cable_layout_parser = create_paremeter_subparsers.add_parser('cable_layout', description=desc, help=desc)

# maisonette' parser
desc = "Create geometrical dimensions of the maisonette."
maisonette_parser = create_paremeter_subparsers.add_parser('maisonette', description=desc, help=desc)

# room' parser
desc = "Create geometrical dimensions of the room."
room_parser = create_paremeter_subparsers.add_parser('room', description=desc, help=desc)

# source' parser
desc = "Create the geometrical dimensions/measures on the source."
source_parser = create_paremeter_subparsers.add_parser('source', description=desc, help=desc)

# feasibility_checkers' parser (which checker to use and their configurations)

# output's parser (format of the outputs) ????


# valid max function maker
def valid_max(name, dtype, max):
    err_msg_template = f"Not a valid {name} max: " + '{s}'
    err_msg_template += f"{name} max must be a {dtype} less than or equal to {max}."

    # define the function to be returned
    def fun(s):

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            arg = dtype(s)

            if not arg <= max:
                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return arg

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


# valid min function maker
def valid_min(name, dtype, min):
    err_msg_template = f"Not a valid {name} min: " + '{s}'
    err_msg_template += f"{name} min must be a {dtype} greater than or equal to {min}."

    # define the function to be returned
    def fun(s):

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            arg = dtype(s)

            if not arg >= min:
                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return arg

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


# valid n for discretisation function maker
def valid_n_discretisation(name, min):
    err_msg_template = f"Not a valid number of {name} to test: " + '{s}'
    err_msg_template += f"It must be an int greater than or equal to {min}."

    def fun(s: str):

        # format the error message template
        err_msg = err_msg_template.format(s=s)

        try:
            # conversion
            i = int(s)

            # check limits
            if not i >= min:

                # raise a arparser's exception
                raise argparse.ArgumentTypeError(err_msg)

            return i

        except Exception:
            # raise a arparser's exception
            raise argparse.ArgumentTypeError(err_msg)

    return fun


def add_discretized_field(parser, name, min, max, min_n):
    # min - help msg
    help_ = f"Minimal value of {name}. Format float >= {min}."

    # min
    parser.add_argument('min_' + name, type=valid_min(name, float, min), help=help_)

    # max - help msg
    help_ = f"Maximal value of {name}. Format float >= {max}."

    # max
    parser.add_argument('max_' + name, type=valid_max(name, float, max), help=help_)

    # nlat - help msg
    help_ = f"Number of {name} values to be tested (from {'min_' + name} to {'max_' + name}). "
    help_ += f"Format: integer >= {min_n}."

    # maxlat - Maximal latitude
    parser.add_argument('n_' + name, type=valid_n_discretisation(name, min_n), help=help_)


# ----------------------------------- create_parameter_parser >>> sun_parser -------------------------------------------
# construction of the sun_parser

# sun's parser (sun trajectories)
desc = "Create a sun's trajectories to test (latitude, maisonette's orientation, #days, #points)."
sun_parser = create_paremeter_subparsers.add_parser('sun', description=desc, help=desc)

# max, min and n values for orientation
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_N_LATITUDE = 1

# latitude args
add_discretized_field(sun_parser, 'latitude', MIN_LATITUDE, MAX_LATITUDE, MIN_N_LATITUDE)

# max, min and n values for orientation
MIN_ORIENTATION = 0.0
MAX_ORIENTATION = 180.0
MIN_N_ORIENTATION = 1


"""
# minlat - help msg
help_ = f"Minimal value of latitude. "
help_ += f"Format: float >= {MIN_LATITUDE} (south)."

# minlat - minimal latitude
sun_parser.add_argument('minlat', type=valid_min('latitude', float, MIN_LATITUDE), help=help_)

# maxlat - help msg
help_ = f"Maximal value of latitude. "
help_ += f"Format: float <= {MAX_LATITUDE:.1f} (north)."

# maxlat - Maximal latitude
sun_parser.add_argument('maxlat', type=valid_max('latitude', float, MAX_LATITUDE), help=help_)

# nlat - help msg
help_ = f"Number of latitude values to be tested (from minlat to maxlat). "
help_ += f"Format: integer >= 1."

# maxlat - Maximal latitude
sun_parser.add_argument('nlat', type=valid_n_discretisation('latitude', MIN_N_LATITUDE), help=help_)
"""

# -------------------------------------------- show_parameter ----------------------------------------------------------


def add_show_parameter_parser(subparsers, parameter):
    help_ = f"Show parameter files for {parameter}."
    parser = subparsers.add_parser(parameter, help=help_)

    help_ = "Alias of particular paremeter file to be shown."
    parser.add_argument('-a', '--alias', type=str, help=help_)


# show_paremeter_subparsers (the different parameters groups)
show_paremeter_subparsers = show_parameter_parser.add_subparsers(metavar='parameter', help='Parameter to show.',
                                                                 dest='parameter')

for param in create_paremeter_subparsers.choices:
    add_show_parameter_parser(show_paremeter_subparsers, param)


# -------------------------------------------- parsing -----------------------------------------------------------------
# namespace (parse the args)
ns = main_parser.parse_args()

print(ns)

# check if the command was given (error message if not)
if not ns.command:
    main_parser.error('No command was passed. Call <<python run.py -h>> for help.')
