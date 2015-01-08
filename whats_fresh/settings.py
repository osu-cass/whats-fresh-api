# flake8: noqa
# This module is how we import settings, and override settings with various
# precedences.

# First our base.py settings module is imported, with all of the
# important defaults.
#
# Next our yaml file is opened, read, and settings defined in the yaml config
# may override settings already defined.

import os
from .base import *


if os.environ['ENVIRONMENTCONFIG']:
    from whats_fresh/environment_config import *
else:
    from .yaml_config import *
