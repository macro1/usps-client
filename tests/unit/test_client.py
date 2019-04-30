import pytest

from usps_client import client, models


def test_standardization_response(standardize_response, mock_pool_manager):
    mock_pool_manager = mock_pool_manager(standardize_response)
    test_client = client.Client("123", pool_manager=mock_pool_manager)

    assert test_client.standardize_address() == models.Address(
        firm_name="USPS OFFICE OF THE CONSUMER ADVOCATE",
        address2="475 LENFANT PLZ SW RM 4012",
        city="WASHINGTON",
        state="DC",
        zip5="20260",
        zip4="0004",
    )


def test_standardization_exception(mock_pool_manager):
    mock_pool_manager = mock_pool_manager(b"<wat></wat>")
    test_client = client.Client("123", pool_manager=mock_pool_manager)

    with pytest.raises(client.APIException):
        next(test_client.standardize_address())


def test_lookup_cities_response(lookup_cities_response, mock_pool_manager):
    mock_pool_manager = mock_pool_manager(lookup_cities_response)
    test_client = client.Client("123", pool_manager=mock_pool_manager)

    assert list(test_client.lookup_cities(["92122", "00000"])) == [
        models.ZipCode(city="SAN DIEGO", state="CA", zip5="92122"),
        None,
    ]


def test_lookup_cities_error(lookup_cities_error, mock_pool_manager):
    mock_pool_manager = mock_pool_manager(lookup_cities_error)
    test_client = client.Client("123", pool_manager=mock_pool_manager)

    with pytest.raises(client.APIException):
        next(test_client.lookup_cities(["abc"]))
