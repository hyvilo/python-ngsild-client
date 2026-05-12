# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from datetime import date, datetime, time
from typing import Self

import pyngsildclient.model.ngsidict as ngsidict
from pyngsildclient.model.constants import AttrType, AttrValue
from pyngsildclient.utils import iso8601


class AttrTemporalValue(ngsidict.NgsiDict):
    @property
    def value(self) -> datetime | date | time:
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        type = self["value"]["@type"]
        value = self["value"]["@value"]
        return iso8601.from_string(type, value)

    @value.setter
    def value(self, v: datetime | date | time):
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        type, value = iso8601.to_string(v)
        self["value"]["@type"] = type
        self["value"]["@value"] = value

    @property
    def type(self):
        return "TemporalProperty"

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> Self:
        property: AttrTemporalValue = cls()
        value = attrV.value
        date_str, temporaltype, _ = iso8601.parse(value)
        v = {
            "@type": temporaltype.value,
            "@value": date_str,
        }
        property["type"] = AttrType.TEMPORAL.value
        property["value"] = v  # set value
        return property
