# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client

from .exceptions import rfc7807_error_handle

logger = logging.getLogger(__name__)


class Types:
    def __init__(self, client: Client, url: str):
        self._client = client
        self._session = client.session
        self.url = url

    @rfc7807_error_handle
    def list(self) -> dict | None:
        r = self._session.get(f"{self.url}")
        return r.json()["typeList"]
