#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import json
from datetime import datetime
from pathlib import Path

from dateutil.tz import UTC

from pyngsildclient.model.entity import Entity
from pyngsildclient.model.helper.openinghours import OpeningHoursBuilder
from pyngsildclient.model.helper.postal import PostalAddressBuilder
from pyngsildclient.utils.urn import Urn


def expected_dict(basename: str) -> dict:
    filename: str = Path(__file__).parent.resolve() / "data" / "urbanmobility" / f"{basename}.json"
    with open(filename) as fp:
        expected = json.load(fp)
    return expected


def test_transportstop():
    """
    https://smart-data-models.github.io/dataModel.UrbanMobility/PublicTransportStop/examples/example-normalized.jsonld
    """
    e = Entity(
        "PublicTransportStop",
        "PublicTransportStop:santander:busStop:463",
        ctx=[
            "https://smart-data-models.github.io/data-models/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )

    e.tprop("dateModified", datetime(2018, 9, 25, 8, 32, 26, tzinfo=UTC))
    e.prop("source", "https://api.smartsantander.eu/")
    e.prop("dataProvider", "http://www.smartsantander.eu/")
    e.prop("entityVersion", "2.0")

    builder = PostalAddressBuilder()
    address = builder.street("C/ La Pereda 14").locality("Santander").region("Cantabria").country("Spain").build()
    e.prop("address", address)

    e.gprop("location", (43.478053126, -3.804648385))
    e.prop("stopCode", "la_pereda_463")
    e.prop("shortStopCode", "463")
    e.prop("name", "La Pereda 14")
    e.prop("wheelchairAccessible", 0)
    e.prop("transportationType", [3])
    e.prop(
        "refPublicTransportRoute",
        [
            "urn:ngsi-ld:PublicTransportRoute:santander:transport:busLine:N3",
            "urn:ngsi-ld:PublicTransportRoute:santander:transport:busLine:N4",
        ],
    )

    e.prop("peopleCount", 0)
    e.prop("refPeopleCountDevice", Urn.prefix("PorpleCountDecice:santander:463"))

    builder = OpeningHoursBuilder()
    openinghours = builder.businessdays("00:01", "23:59").build()
    e.prop("openingHoursSpecification", openinghours)

    assert e.to_dict() == expected_dict("transport_stop")
