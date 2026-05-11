# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from collections.abc import Mapping

from ..ngsidict import NgsiDict
from ..utils import guess_ngsild_type
from .geo import AttrGeoValue
from .prop import AttrPropValue
from .rel import AttrRelValue
from .temporal import AttrTemporalValue


class AttrFactory:
    @classmethod
    def create(self, attr: Mapping) -> NgsiDict:
        try:
            type = guess_ngsild_type(attr)
        except ValueError:
            return attr
        if type == "Property":
            return AttrPropValue(attr)
        elif type == "TemporalProperty":
            return AttrTemporalValue(attr)
        elif type == "GeoProperty":
            return AttrGeoValue(attr)
        elif type == "Relationship":
            return AttrRelValue(attr)
        else:
            return NgsiDict(attr)  # should happen only for json arrays
