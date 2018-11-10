from usps_client import client


def test_zip_lookup(usps_client):

    [address_result] = usps_client.standardize_address(
        firm_name="USPS Office of the Consumer Advocate",
        address="475 LENFANT PLZ SW RM 4012",
        city="Washington",
        state="DC",
        zip="20260",
    )
    assert address_result == {
        "FirmName": "USPS OFFICE OF THE CONSUMER ADVOCATE",
        "Address2": "475 LENFANT PLZ SW RM 4012",
        "City": "WASHINGTON",
        "State": "DC",
        "Zip5": "20260",
        "Zip4": "0004",
    }
