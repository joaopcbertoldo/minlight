# -*- coding: utf-8 -*-
"""
Main.
"""

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
from src.simulation.field_tension_compromise.parsing import get_main_parser


# main_parser
main_parser = get_main_parser()

# parsing
# namespace (parse the args)
ns = main_parser.parse_args(sys.argv[1:])

print(ns)

# check if the command was given (error message if not)
if not ns.command:
    main_parser.error('No command was passed. Call <<python run.py -h>> for help.')
