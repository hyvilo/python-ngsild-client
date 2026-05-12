# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
from datetime import datetime
from typing import Any, Self

import pyngsildclient
from pyngsildclient.model.utils import iso8601, process_observedat

from ...utils.urn import Urn
from ..constants import META_ATTR_DATASET_ID, META_ATTR_OBSERVED_AT, META_ATTR_UNITCODE, AttrType, AttrValue
from ..exceptions import NgsiUnmatchedAttributeTypeError


class AttrPropValue(pyngsildclient.model.ngsidict.NgsiDict):
    @property
    def type(self):
        return "Property"

    @property
    def value(self) -> Any:
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        return self["value"]

    @value.setter
    def value(self, v: Any):
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        self["value"] = v

    @property
    def observedat(self) -> datetime:
        dt: str = self.get("observedAt")
        if dt:
            return iso8601.to_datetime(dt)
        return

    @observedat.setter
    def observedat(self, dt: datetime):
        self["observedAt"] = iso8601.from_datetime(dt)

    @property
    def unitcode(self) -> str:
        return self.get("unitCode")

    @unitcode.setter
    def unitcode(self, unitcode: str):
        self["unitcode"] = unitcode

    @property
    def datasetid(self) -> str:
        return self.get("datasetId")

    @datasetid.setter
    def datasetid(self, datasetid: str):
        self["datasetId"] = Urn.prefix(datasetid)

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> Self:
        property: AttrPropValue = cls()
        value = attrV.value
        if isinstance(value, (int, float, bool, str, list, dict)):
            v = value
        else:
            raise NgsiUnmatchedAttributeTypeError(f"Cannot map {type(value)} to NGSI type. {value=}")
        property["type"] = AttrType.PROP.value  # set type
        property["value"] = v  # set value
        if attrV.unitcode is not None:
            property[META_ATTR_UNITCODE] = attrV.unitcode
        if attrV.observedat is not None:
            property[META_ATTR_OBSERVED_AT] = process_observedat(attrV.observedat)
        if attrV.datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(attrV.datasetid)
        if attrV.userdata:
            property |= attrV.userdata
        return property
