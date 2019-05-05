from usps_client import models


def test_standardize_address(usps_client):

    assert usps_client.standardize_address(
        firm_name="USPS Office of the Consumer Advocate",
        address1="475 LENFANT PLZ SW RM 4012",
        city="Washington",
        state="DC",
        zip5="20260",
    ) == models.Address(
        firm_name="USPS OFFICE OF THE CONSUMER ADVOCATE",
        address2="475 LENFANT PLZ SW RM 4012",
        city="WASHINGTON",
        state="DC",
        zip5="20260",
        zip4="0004",
    )


def test_lookup_zip_code(usps_client):

    assert usps_client.lookup_zip_code(
        firm_name="USPS Office of the Consumer Advocate",
        address1="475 LENFANT PLZ SW RM 4012",
        city="Washington",
        state="DC",
        zip5="20261",
    ) == models.Address(
        firm_name="USPS OFFICE OF THE CONSUMER ADVOCATE",
        address2="475 LENFANT PLZ SW RM 4012",
        city="WASHINGTON",
        state="DC",
        zip5="20260",
        zip4="0004",
    )


def test_lookup_city(usps_client):

    assert usps_client.lookup_city("20260") == models.ZipCode(
        zip5="20260", city="WASHINGTON", state="DC"
    )
