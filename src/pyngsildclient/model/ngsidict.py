# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal, Optional, Union

from .constants import AttrValue, MultAttrValue, NgsiDate

if TYPE_CHECKING:
    from pyngsildclient.model.attr.geo import AttrGeoValue
    from pyngsildclient.model.attr.prop import AttrPropValue
    from pyngsildclient.model.attr.rel import AttrRelValue
    from pyngsildclient.model.attr.temporal import AttrTemporalValue
    from pyngsildclient.model.entity import Entity

    from .constants import NgsiGeometry

import json
from collections.abc import Mapping, MutableMapping
from copy import deepcopy

from geojson import Point
from scalpl import Cut

from ..utils import iso8601, url

"""
This module contains the definition of the NgsiDict class.
"""


class NgsiDict(Cut, MutableMapping):
    """This class is a custom dictionary that backs an entity.

    Attr is used to build and hold the entity properties, as well as the entity's root.
    It's not exposed to the user but intended to be used by the Entity class.
    NgsiDict provides methods that allow to build a dictionary compliant with a NGSI-LD structure.

    See Also
    --------
    model.Entity
    """

    def __init__(self, data: dict | None = None, name: str | None = None):
        super().__init__(data)
        self.name = name

    def is_root(self) -> bool:
        return self.get("@context") is not None

    def __getitem__(self, path: str):
        item = super().__getitem__(path)
        if isinstance(item, Mapping) and not isinstance(item, NgsiDict):
            from pyngsildclient.model.attr.factory import AttrFactory

            return AttrFactory.create(item)
        return item

    def get(self, path: str, default=None):
        try:
            item = super().__getitem__(path)
        except (KeyError, IndexError):
            return default
        if isinstance(item, Mapping) and not isinstance(item, NgsiDict):
            from pyngsildclient.model.attr.factory import AttrFactory

            return AttrFactory.create(item)
        return item

    def __repr__(self):
        return self.data.__repr__()

    def __ior__(self, prop: Mapping):
        prop = prop.data if isinstance(prop, NgsiDict) else prop
        self.data |= prop
        return self

    def __mul__(self, n: int):
        res = []
        for _ in range(n):
            res.append(NgsiDict.duplicate(self))
        return res

    __rmul__ = __mul__

    @classmethod
    def duplicate(cls, attr: "NgsiDict") -> "NgsiDict":
        return deepcopy(attr)

    def dup(self) -> "NgsiDict":
        """Duplicates the NgsiDict

        Returns
        -------
        Entity
            The new entity
        """
        return deepcopy(self)

    @property
    def value(self):
        raise NotImplementedError()

    @value.setter
    def value(self, v: Any):
        raise NotImplementedError()

    @property
    def type(self) -> Literal["Property", "GeoProperty", "TemporalProperty", "Relationship"]:
        raise NotImplementedError()

    @classmethod
    def _from_json(cls, payload: str):
        d = json.loads(payload)
        return cls(d)

    @classmethod
    def _load(cls, filename: str):
        with open(filename) as fp:
            d = json.load(fp)
            return cls(d)

    def to_dict(self) -> dict:
        return self.data

    def to_json(self, pattern: str | None = None, indent: int = None) -> str:
        """Returns the dict in json format"""
        if pattern:
            pattern = pattern.lower()
        d = {k: v for k, v in self.items() if pattern in k.lower()} if pattern else self
        return json.dumps(
            d, ensure_ascii=False, indent=indent, default=lambda x: x.data if isinstance(x, NgsiDict) else str
        )

    def pprint(self, *args, **kwargs) -> None:
        """Returns the dict pretty-json-formatted"""
        from pyngsildclient.settings import globalsettings

        globalsettings.f_print(self.to_json(*args, indent=2, **kwargs))

    def _save(self, filename: str, indent=2):
        with open(filename, "w") as fp:
            json.dump(
                self,
                fp,
                ensure_ascii=False,
                indent=indent,
                default=lambda x: x.data if isinstance(x, NgsiDict) else str,
            )

    @classmethod
    def mkprop(
        cls,
        value: Any,
        *,  # keyword-only arguments after this
        datasetid: str | None = None,
        observedat: str | None | datetime = None,
        unitcode: str | None = None,
        userdata: Optional["NgsiDict"] = None,
        escape: bool = False,
        attrname: str | None = None,
    ) -> "AttrPropValue":
        from pyngsildclient.model.attr.prop import AttrPropValue

        if isinstance(value, MultAttrValue):
            if len(value) == 0:
                raise ValueError("MultAttr is empty")
            p: list[AttrPropValue] = [AttrPropValue.build(v) for v in value]
        else:
            value = url.escape(value) if escape and isinstance(value, str) else value
            attrvalue = AttrValue(value, datasetid, observedat, unitcode, userdata)
            p = AttrPropValue.build(attrvalue)
        return {attrname: p} if attrname else p

    @classmethod
    def mkgprop(
        cls,
        value: Union[tuple[float], "NgsiGeometry"],
        *,  # keyword-only arguments after this
        datasetid: str | None = None,
        observedat: str | datetime | None = None,
        attrname: str | None = None,
        precision: int = 6,
    ) -> "AttrGeoValue":
        from pyngsildclient.model.attr.geo import AttrGeoValue

        if isinstance(value, tuple):
            if len(value) == 2:
                lat, lon = value
                value = Point((lon, lat), precision=precision)
            else:
                raise ValueError("lat, lon tuple expected")
        attrvalue = AttrValue(value, datasetid, observedat)
        p = AttrGeoValue.build(attrvalue)
        return {attrname: p} if attrname else p

    @classmethod
    def mktprop(
        cls,
        value: NgsiDate | None = None,
        *,  # keyword-only arguments after this
        attrname: str | None = None,
    ) -> "AttrTemporalValue":
        from pyngsildclient.model.attr.temporal import AttrTemporalValue

        value = value or iso8601.utcnow()

        attrvalue = AttrValue(value)
        p = AttrTemporalValue.build(attrvalue)
        return {attrname: p} if attrname else p

    @classmethod
    def mkrel(
        cls,
        value: str | list[str] | Entity | list[Entity],
        *,  # keyword-only arguments after this
        datasetid: str | None = None,
        observedat: str | datetime | None = None,
        attrname: str | None = None,
    ) -> "AttrRelValue":
        from pyngsildclient.model.attr.rel import AttrRelValue

        if isinstance(value, MultAttrValue):
            if len(value) == 0:
                raise ValueError("MultAttr is empty")
            p: list[AttrRelValue] = [AttrRelValue.build(v.id if hasattr(v, "id") else v) for v in value]
        else:
            value = value.id if hasattr(value, "id") else value
            attrvalue = AttrValue(value, datasetid, observedat)
            p = AttrRelValue.build(attrvalue)
        return {attrname: p} if attrname else p
