# Copyright (C) 2025 https://github.com/FranBarInstance/neutral-starter-py (See LICENCE)

"""Tests package for hellocomp component."""

import os
import sys

# Add component root and route to sys.path to allow imports without hardcoded component name
_base_dir = os.path.dirname(os.path.abspath(__file__))
_comp_dir = os.path.dirname(_base_dir)
_route_dir = os.path.join(_comp_dir, 'route')

if _route_dir not in sys.path:
    sys.path.insert(0, _route_dir)
