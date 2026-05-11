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
    from .client import AsyncClient

from ..exceptions import rfc7807_error_handle_async

logger = logging.getLogger(__name__)


class Types:
    def __init__(self, client: AsyncClient, url: str):
        self._client = client
        self.url = url

    @rfc7807_error_handle_async
    async def list(self) -> dict | None:
        r = await self._client.client.get(f"{self.url}")
        return r.json()["typeList"]
