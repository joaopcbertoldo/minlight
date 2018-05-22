# -*- coding: utf-8 -*-
"""
Main.
"""

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
from src.simulation.field_tension_compromise.parsing import _main_parser


def get_main_parser():
    return _main_parser.main_parser
