# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import typing
from collections.abc import Callable
from dataclasses import dataclass

from rich import print_json

from pyngsildclient.utils import is_interactive

if typing.TYPE_CHECKING:
    from pyngsildclient.api.follow import LinkFollower


@dataclass
class Settings:
    """The default settings used to build an Entity"""

    autoprefix: bool = True
    """A boolean to enable/disable the automatic insertion of the type into the identifier.
    Default is enabled.
    """

    strict: bool = False  # for future use
    autoescape: bool = True  # for future use
    f_print: Callable = print
    follower: "LinkFollower" = None

    def __post_init__(self):
        if is_interactive():
            self.f_print = print_json


globalsettings: Settings = Settings()
