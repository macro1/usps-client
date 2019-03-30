# usps-client

[![CircleCI](https://img.shields.io/circleci/project/github/macro1/usps-client.svg)](https://circleci.com/gh/macro1/usps-client)
[![Known Vulnerabilities](https://img.shields.io/snyk/vulnerabilities/github/macro1/usps-client.svg)](https://snyk.io/test/github/macro1/usps-client?targetFile=requirements.txt)

Python client for the USPS Web Tools API.

## Usage

Import the client, instantiate with your user id (register at https://registration.shippingapis.com/)
and call the standardize method:
```python
from usps_client.client import Client

usps = Client('[your user id]')
standardized = usps.standardize_address(
    firm_name="USPS Office of the Consumer Advocate",
    address="475 LENFANT PLZ SW RM 4012",
    city="Washington",
    state="DC",
    zip="20260",
)
```
A dictionary will be returned containing the API response from USPS.