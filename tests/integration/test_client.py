from __future__ import unicode_literals

from usps_client import models


def test_standardize_address(usps_client):

    assert usps_client.standardize_address(
        firm_name="USPS Office of the Consumer Advocate",
        address1="475 LENFANT PLZ SW RM 4012",
        city="Washington",
        state="DC",
        zip5="20260",
    ) == models.ResponseAddress(
        firm_name="USPS OFFICE OF THE CONSUMER ADVOCATE",
        address2="475 LENFANT PLZ SW RM 4012",
        city="WASHINGTON",
        state="DC",
        zip5="20260",
        zip4="0004",
        return_text="Default address: The address you entered was found but more information is needed (such as an apartment, suite, or box number) to match to a specific address.",
        delivery_point="99",
        carrier_route="C000",
        footnotes="S",
        dpv_confirmation="S",
        dpvcmra="N",
        dpv_footnotes="AACC",
        business="Y",
        central_delivery_point="N",
        vacant="N",
    )


def test_standardize_address_city_abbrev(usps_client):

    assert usps_client.standardize_address(
        address1="100 Kercheval Ave",
        city="Grosse Pointe Farms",
        state="MI",
        zip5="48236",
    ) == models.ResponseAddress(
        firm_name="",
        address2="100 KERCHEVAL AVE",
        city="GROSSE POINTE FARMS",
        city_abbreviation="GROSSE PT FRM",
        state="MI",
        zip5="48236",
        zip4="3635",
        return_text="Default address: The address you entered was found but more information is needed (such as an apartment, suite, or box number) to match to a specific address.",
        delivery_point="99",
        carrier_route="C026",
        footnotes="H",
        dpv_confirmation="D",
        dpvcmra="N",
        dpv_footnotes="AAN1",
        business="N",
        central_delivery_point="N",
        vacant="N",
    )


def test_standardize_address_no_zip4(usps_client):

    assert usps_client.standardize_address(
        address1="220 main ave", city="gaylord", state="mn", zip5="44334"
    ) == models.ResponseAddress(
        address2="220 MAIN AVE",
        city="GAYLORD",
        state="MN",
        zip5="55334",
        zip4="9618",
        delivery_point="20",
        carrier_route="R002",
        footnotes="A",
        dpv_confirmation="Y",
        dpvcmra="N",
        dpv_footnotes="AABB",
        business="Y",
        central_delivery_point="N",
        vacant="N",
    )


def test_standardize_no_result(usps_client):

    assert (
        usps_client.standardize_address(
            address1="202 us highway 1", city="falmouth", state="me"
        )
        is None
    )


def test_lookup_zip_code(usps_client):

    assert usps_client.lookup_zip_code(
        firm_name="USPS Office of the Consumer Advocate",
        address1="475 LENFANT PLZ SW RM 4012",
        city="Washington",
        state="DC",
        zip5="20261",
    ) == models.ResponseAddress(
        firm_name="USPS OFFICE OF THE CONSUMER ADVOCATE",
        address2="475 LENFANT PLZ SW RM 4012",
        city="WASHINGTON",
        state="DC",
        zip5="20260",
        zip4="0004",
        return_text="Default address: The address you entered was found but more information is needed (such as an apartment, suite, or box number) to match to a specific address.",
    )


def test_lookup_city(usps_client):

    assert usps_client.lookup_city("20260") == models.ZipCode(
        zip5="20260", city="WASHINGTON", state="DC"
    )


def test_domestic_rate(usps_client):
    response_package = usps_client.domestic_rate(
        service="PRIORITY",
        zip_origination="20260",
        zip_destination="01111",
        size="LARGE",
        pounds="0",
        ounces="1.23",
        width="15",
        length="30",
        height="15",
        girth="55",
    )
    # skip checking a couple attributes that tend to change a lot
    response_package.postage.special_services = None
    response_package.postage.rate = None

    assert response_package == models.ResponsePackage(
        zip_origination="20260",
        zip_destination="01111",
        pounds="0",
        ounces="1.23",
        container="VARIABLE",
        size=None,
        zone="3",
        postage=models.Postage(
            mail_service="Priority Mail 2-Day\u2122",
            rate=None,
            special_services=None,
        ),
    )
