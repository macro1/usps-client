import os

import pytest


@pytest.fixture
def user_id():
    return os.environ["USER_ID"]


@pytest.fixture
def usps_client(user_id):
    from usps_client.client import Client

    return Client(user_id)
