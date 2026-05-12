# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

"""
This module contains helper functions to generate temporal query params.

Notes
-----
NGSI-LD dates are expressed in UTC, using the ISO8601 format.

References
----------
.. [1] ETSI, 2021. "Supported data types for Values" in Context Information Management (CIM); NGSI-LD API
    ETSI GS CIM 009 V1.4.2, pp. 41-42, 2021-04.
"""

from datetime import UTC, datetime, timedelta

from pyngsildclient.api.constants import TimeProperty
from pyngsildclient.utils.iso8601 import from_datetime


class TemporalQuery(dict):
    def __init__(self):
        super().__init__()

    def after(
        self, start: datetime | timedelta | str = timedelta(days=30), timeprop: TimeProperty | None = None
    ) -> dict:
        self["timerel"] = "after"
        if isinstance(start, timedelta):
            self["timeAt"] = from_datetime(datetime.utcnow() - start)
        elif isinstance(start, datetime):
            self["timeAt"] = from_datetime(start)
        else:
            self["timeAt"] = start
        if timeprop is not None:
            self["timeproperty"] = timeprop.value
        return self

    def before(self, end: datetime | str | None = None, timeprop: TimeProperty | None = None) -> dict:
        end = end or datetime.now(UTC)

        self["timerel"] = "before"
        self["timeAt"] = from_datetime(end) if isinstance(end, datetime) else end
        if timeprop is not None:
            self["timeproperty"] = timeprop.value
        return self

    def between(self, start: datetime | str, end: datetime | str, timeprop: TimeProperty | None = None) -> dict:
        self["timerel"] = "between"
        self["timeAt"] = from_datetime(start) if isinstance(start, datetime) else start
        self["endTimeAt"] = from_datetime(end) if isinstance(end, datetime) else end
        if timeprop is not None:
            self["timeproperty"] = timeprop.value
        return self
