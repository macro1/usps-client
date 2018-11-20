def test_zip_lookup(usps_client):

    assert usps_client.standardize_address(
        firm_name="USPS Office of the Consumer Advocate",
        address="475 LENFANT PLZ SW RM 4012",
        city="Washington",
        state="DC",
        zip="20260",
    ) == {
        "FirmName": "USPS OFFICE OF THE CONSUMER ADVOCATE",
        "Address2": "475 LENFANT PLZ SW RM 4012",
        "City": "WASHINGTON",
        "State": "DC",
        "Zip5": "20260",
        "Zip4": "0004",
    }
