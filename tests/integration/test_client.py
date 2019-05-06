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

    assert usps_client.domestic_rate(
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
    ) == models.ResponsePackage(
        zip_origination="20260",
        zip_destination="01111",
        pounds="0",
        ounces="1.23",
        container="VARIABLE",
        size="LARGE",
        zone="3",
        postage=models.Postage(
            mail_service="Priority Mail 2-Day\u2122",
            rate="7.70",
            special_services=[
                models.SpecialService(
                    service_id="119",
                    service_name="Adult Signature Required",
                    available="true",
                    price="6.40",
                ),
                models.SpecialService(
                    service_id="120",
                    service_name="Adult Signature Restricted Delivery",
                    available="true",
                    price="6.66",
                ),
                models.SpecialService(
                    service_id="104",
                    service_name="Certificate of Mailing (Form 3817)",
                    available="true",
                    price="1.45",
                ),
                models.SpecialService(
                    service_id="105",
                    service_name="Certified Mail\xae",
                    available="true",
                    price="3.50",
                ),
                models.SpecialService(
                    service_id="170",
                    service_name="Certified Mail\xae Restricted Delivery",
                    available="true",
                    price="8.80",
                ),
                models.SpecialService(
                    service_id="171",
                    service_name="Certified Mail\xae Adult Signature Required",
                    available="true",
                    price="8.80",
                ),
                models.SpecialService(
                    service_id="172",
                    service_name="Certified Mail\xae Adult Signature Restricted Delivery",
                    available="true",
                    price="8.80",
                ),
                models.SpecialService(
                    service_id="103",
                    service_name="Collect on Delivery",
                    available="true",
                    price="7.75",
                    declared_value_required="true",
                    due_sender_required="false",
                ),
                models.SpecialService(
                    service_id="175",
                    service_name="Collect on Delivery Restricted Delivery",
                    available="true",
                    price="12.95",
                    declared_value_required="true",
                    due_sender_required="false",
                ),
                models.SpecialService(
                    service_id="125",
                    service_name="Insurance",
                    available="true",
                    price="0.00",
                    declared_value_required="true",
                    due_sender_required="false",
                ),
                models.SpecialService(
                    service_id="179",
                    service_name="Insurance Restricted Delivery",
                    available="true",
                    price="0.00",
                    declared_value_required="true",
                    due_sender_required="false",
                ),
                models.SpecialService(
                    service_id="109",
                    service_name="Registered Mail\u2122",
                    available="true",
                    price="12.40",
                    declared_value_required="true",
                    due_sender_required="false",
                ),
                models.SpecialService(
                    service_id="176",
                    service_name="Registered Mail\u2122 Restricted Delivery",
                    available="true",
                    price="17.60",
                    declared_value_required="true",
                    due_sender_required="false",
                ),
                models.SpecialService(
                    service_id="107",
                    service_name="Return Receipt for Merchandise",
                    available="true",
                    price="4.30",
                ),
                models.SpecialService(
                    service_id="108",
                    service_name="Signature Confirmation\u2122",
                    available="true",
                    price="3.05",
                ),
                models.SpecialService(
                    service_id="173",
                    service_name="Signature Confirmation\u2122 Restricted Delivery",
                    available="true",
                    price="8.25",
                ),
                models.SpecialService(
                    service_id="156",
                    service_name="Signature Confirmation\u2122 Electronic",
                    available="true",
                    price="2.60",
                ),
                models.SpecialService(
                    service_id="174",
                    service_name="Signature Confirmation\u2122 Electronic Restricted Delivery",
                    available="true",
                    price="7.80",
                ),
                models.SpecialService(
                    service_id="190",
                    service_name="Special Handling - Fragile",
                    available="true",
                    price="10.95",
                ),
                models.SpecialService(
                    service_id="106",
                    service_name="USPS Tracking\xae",
                    available="true",
                    price="0.00",
                ),
                models.SpecialService(
                    service_id="155",
                    service_name="USPS Tracking\xae Electronic",
                    available="true",
                    price="0.00",
                ),
            ],
        ),
    )
