# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
from collections.abc import Sequence
from datetime import datetime
from typing import Self

import pyngsildclient
from pyngsildclient.model.utils import iso8601, process_observedat

from ...utils.urn import Urn
from ..constants import META_ATTR_DATASET_ID, META_ATTR_OBSERVED_AT, AttrType, AttrValue
from ..exceptions import NgsiUnmatchedAttributeTypeError


class AttrRelValue(pyngsildclient.model.ngsidict.NgsiDict):
    @property
    def type(self):
        return "Relationship"

    @property
    def value(self):
        if self["type"] != "Relationship":
            raise ValueError("Attribute type MUST be Relationship")
        return self["object"]

    @value.setter
    def value(self, v: str):
        if self["type"] != "Relationship":
            raise ValueError("Attribute type MUST be Relationship")
        self["object"] = Urn.prefix(v)

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
        property: AttrRelValue = cls()
        value = attrV.value
        if isinstance(value, str):
            value = Urn.prefix(value)
        elif isinstance(value, Sequence):
            value = [Urn.prefix(v) for v in value]
        else:
            raise NgsiUnmatchedAttributeTypeError(f"Cannot map {type(value)} to NGSI type. {value=}")
        property["type"] = AttrType.REL.value  # set type
        property["object"] = value  # set value
        if attrV.observedat is not None:
            property[META_ATTR_OBSERVED_AT] = process_observedat(attrV.observedat)
        if attrV.datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(attrV.datasetid)
        return property
