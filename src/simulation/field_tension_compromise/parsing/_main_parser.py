# -*- coding: utf-8 -*-
"""
Main.
"""

# imports
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
from src.simulation.field_tension_compromise.defaults import Constants as Const
from src.simulation.field_tension_compromise.parsing import _factory as fac


# ----------------------------------------------- 0 main ---------------------------------------------------------------
# construction of the main_parser

# 0 - the main main_parser (which holds several parsers for the commands)
main_parser = argparse.ArgumentParser(prog='field_tension_compromise',
                                      description='This program will configure the necessary inputs for the '
                                                  'field-tension compromise workflow and call runs for it.')

# 0 - debug option
main_parser.add_argument('--debug', action='store_true', help='Show debug messages.')

# 0 -> 0.* - main_subparsers (the commands)
main_subparsers = main_parser.add_subparsers(metavar='command', help='Command to execute.', dest='command')

# 0.1 - create_parameter_parser
desc = 'Create a parameter file for the workflow.'
create_parameter_parser = main_subparsers.add_parser('create_parameter', description=desc, help=desc)

# 0.2 - show_parameter_parser
desc = 'Show the available parameter files or their contents.'
show_parameter_parser = main_subparsers.add_parser('show_parameter', description=desc, help=desc)


# -------------------------------------------- 0.1 create_parameter ----------------------------------------------------
# construction of the create_parameter_parser

# debug option
# create_parameter_parser.add_argument('--debug', action='store_true', help='Show debug messages.')

# 0.1 -> 0.1.* - create_paremeter_subparsers (the different parameters groups)
create_paremeter_subparsers = create_parameter_parser.add_subparsers(metavar='parameter', help='Parameter to create.',
                                                                     dest='parameter')

# 0.1.1 - spherical's parser (spherical reference system)
desc = "Create a spherical reference system for the window (position and orientation)."
spherical_parser = create_paremeter_subparsers.add_parser('spherical', description=desc, help=desc)

# 0.1.2 - rho_roll_liberty's parser
# (range where rho and roll can vary to search feasible positions)
desc = "Create a rho and roll liberty field (2D range to search possible positions)."
rho_roll_liberty_parser = create_paremeter_subparsers.add_parser('rho_roll_liberty', description=desc, help=desc)

# 0.1.3 - fixation's parser (fixation's positions to test)
desc = "Create a set of fixation positions to test."
fixation_parser = create_paremeter_subparsers.add_parser('fixation', description=desc, help=desc)

# 0.1.4 - cable_layout's parser (set of cable layouts to test)
desc = "Create a set of cable layouts to test."
cable_layout_parser = create_paremeter_subparsers.add_parser('cable_layout', description=desc, help=desc)

# 0.1.5 - maisonette' parser
desc = "Create geometrical dimensions of the maisonette."
maisonette_parser = create_paremeter_subparsers.add_parser('maisonette', description=desc, help=desc)

# 0.1.6 - room' parser
desc = "Create geometrical dimensions of the room."
room_parser = create_paremeter_subparsers.add_parser('room', description=desc, help=desc)

# 0.1.7 - source' parser
desc = "Create the geometrical dimensions/measures on the source."
source_parser = create_paremeter_subparsers.add_parser('source', description=desc, help=desc)

# 0.1.8 - sun's parser (sun trajectories)
desc = "Create a set of sun trajectories to test (latitude, maisonette's orientation, #days, #points)."
sun_parser = create_paremeter_subparsers.add_parser('sun', description=desc, help=desc)


# -------------------------------------------- 0.1.1 spherical ---------------------------------------------------------

# 0.1.1.0 - alias
fac.add_alias_argument(spherical_parser)

# 0.1.1.1 - alias
# fac.add_borned_float_argument(spherical_parser)


# -------------------------------------------- 0.1.8 sun ---------------------------------------------------------------

# 0.1.8.0 - alias
fac.add_alias_argument(sun_parser)

# 0.1.8.1  - latitude args
fac.add_discretized_real_field(sun_parser, 'latitude',
                               Const.MIN_LATITUDE, Const.MAX_LATITUDE, Const.MIN_N_LATITUDE)

# 0.1.8.2 - orientation args
fac.add_discretized_real_field(sun_parser, 'orientation',
                               Const.MIN_ORIENTATION, Const.MAX_ORIENTATION, Const.MIN_N_ORIENTATION)

# 0.1.8.3 - #points per trajectory
fac.add_borned_int_argument(sun_parser, 'n_points_trajectory',
                            Const.MIN_N_POINTS_TRAJECTORY, Const.MAX_N_POINTS_TRAJECTORY)

# 0.1.8.4.* - days of the year
days_year_group = sun_parser.add_mutually_exclusive_group(required=True)

# 0.1.8.4.A - n days of the year
fac.add_borned_int_argument(days_year_group, '--n_days_year',
                            Const.FIRST_DAY_YEAR, Const.LAST_DAY_YEAR)

# 0.1.8.4.B - list of days of the year
fac.add_borned_int_list_argument(days_year_group, '--days_year',
                                 Const.FIRST_DAY_YEAR, Const.LAST_DAY_YEAR)


# -------------------------------------------- show_parameter ----------------------------------------------------------

# 0.2 -> 0.2.* -  show_paremeter_subparsers (the different parameters groups)
show_paremeter_subparsers = show_parameter_parser.add_subparsers(metavar='parameter', help='Parameter to show.',
                                                                 dest='parameter')

# 0.2.* - add the subparsers
fac.add_show_parameter_parsers(create_paremeter_subparsers, show_paremeter_subparsers)
