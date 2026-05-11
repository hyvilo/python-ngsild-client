# Software Name: pyngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from pytest import fixture
from pytest_mock import MockerFixture


@fixture()
def mocked_connected(mocker: MockerFixture):
    import pyngsildclient.api.client

    mocker.patch.object(pyngsildclient.api.client.Client, "is_connected", return_value=True)
