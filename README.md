# usps-client

[![CircleCI](https://img.shields.io/circleci/project/github/macro1/usps-client.svg)](https://circleci.com/gh/macro1/usps-client)
[![Known Vulnerabilities](https://img.shields.io/snyk/vulnerabilities/github/macro1/usps-client.svg)](https://snyk.io/test/github/macro1/usps-client?targetFile=requirements.txt)

Python client for the USPS Web Tools API.

## Usage

Import the client, instantiate with your user id (register at https://registration.shippingapis.com/)
and call the standardize method:
```python
>>> import usps_client
>>> usps = usps_client.Client('[your user id]')
>>> standardized = usps.standardize_address(
...     firm_name="USPS Office of the Consumer Advocate",
...     address1="475 LENFANT PLZ SW RM 4012",
...     city="Washington",
...     state="DC",
...     zip5="20260",
... )
```
An Address object will be returned, containing data returned from the USPS Web Tools API.

Since the return classes are defined using the attrs model, it is possible to convert into generic types:
```python
>>> import attr
>>> attr.asdict(standardized)
{'firm_name': 'USPS OFFICE OF THE CONSUMER ADVOCATE', 'address1': None, 'address2': '475 LENFANT PLZ SW RM 4012', 'city': 'WASHINGTON', 'state': 'DC', 'zip5': '20260', 'zip4': '0004'}
```
