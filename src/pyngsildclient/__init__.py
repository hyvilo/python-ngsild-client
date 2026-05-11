"""
Software Name: pyngsildclient
SPDX-FileCopyrightText: Copyright (c) 2021 Orange
SPDX-License-Identifier: Apache 2.0

This software is distributed under the Apache 2.0;
see the NOTICE file for more details.

Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
"""

import http.client
import logging
import sys

__version__ = "0.6.0"

from .utils import is_interactive

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
if is_interactive():
    logging.disable(logging.CRITICAL)
    sys.tracebacklimit = 0

logger = logging.getLogger(__name__)

http.client.HTTPConnection.debuglevel = 1


def print_to_log(*args):
    logger.debug(" ".join(args))


# monkey patch the http.client's print() function
http.client.print = print_to_log
