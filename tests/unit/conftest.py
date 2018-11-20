import os

import pytest


@pytest.fixture
def fixture_path():
    return os.path.sep.join([os.path.dirname(__file__), "fixtures"])


@pytest.fixture
def standardize_response(fixture_path):
    with open(
        os.path.sep.join([fixture_path, "standardize_response.xml"]), mode="rb"
    ) as infile:
        content = infile.read()
    return content


@pytest.fixture
def lookup_cities_response(fixture_path):
    with open(
        os.path.sep.join([fixture_path, "lookup_cities_response.xml"]), mode="rb"
    ) as infile:
        content = infile.read()
    return content


@pytest.fixture
def lookup_cities_error(fixture_path):
    with open(
        os.path.sep.join([fixture_path, "lookup_cities_error.xml"]), mode="rb"
    ) as infile:
        content = infile.read()
    return content


@pytest.fixture
def mock_pool_manager():
    from urllib3 import response

    class MockPoolManager:
        def __init__(self, mock_response):
            self.mock_response = mock_response

        def request(self, *args, **kwargs):
            return response.HTTPResponse(body=self.mock_response)

        def clear(self):
            pass

    return MockPoolManager
