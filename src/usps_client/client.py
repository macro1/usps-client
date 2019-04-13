import io
import itertools
import logging

import certifi
import urllib3

from . import etree, models

try:
    import typing
except ImportError:
    pass

logger = logging.getLogger()


def grouper(iterable):
    iterable = iter(iterable)

    def just_five(iterable):
        return list(itertools.islice(iterable, 5))

    while True:
        next_group = just_five(iterable)
        if not next_group:
            return
        yield next_group


class APIException(Exception):
    def __init__(self, element):
        if not isinstance(element, type(etree.ElementTree())):
            element = etree.ElementTree(element)
        xml_buffer = io.BytesIO()
        element.write(xml_buffer)
        super(APIException, self).__init__(xml_buffer.getvalue())


class Client:
    BASE_URL = "https://secure.shippingapis.com/ShippingAPI.dll"
    ENCODING = "iso-8859-1"

    def __init__(self, user_id, pool_manager=None):
        self.user_id = user_id
        if pool_manager is None:
            self.pool_manager = urllib3.PoolManager(
                cert_reqs="CERT_REQUIRED", ca_certs=certifi.where()
            )
        else:
            self.pool_manager = pool_manager

    def request(self, api, element_tree):
        # type: (str, etree.ElementTree) -> etree.ElementTree
        element_tree.getroot().set("USERID", self.user_id)

        xml_buffer = io.BytesIO()

        element_tree.write(xml_buffer, method="html", encoding=self.ENCODING)
        response = self.pool_manager.request(
            "GET", self.BASE_URL, fields={"API": api, "XML": xml_buffer.getvalue()}
        )
        self.pool_manager.clear()

        response_tree = etree.ElementTree()
        response_tree.parse(
            io.BytesIO(response.data), etree.XMLParser(encoding=self.ENCODING)
        )
        return response_tree

    def standardize_addresses(self, addresses):
        # type: (typing.Iterable[models.Address]) -> typing.Iterable[models.Address]
        for address_group in grouper(addresses):
            request_element = etree.Element("AddressValidateRequest")
            for address_id, raw_address in enumerate(address_group):
                address_element = raw_address.xml()
                address_element.set("ID", "{}".format(address_id))
                request_element.append(address_element)

            response_tree = self.request(
                "Verify", etree.ElementTree(request_element)
            ).getroot()

            if response_tree.tag == "AddressValidateResponse":
                for address_result in response_tree:
                    address = models.Address.from_xml(address_result)
                    print(address)
                    yield address
            else:
                raise APIException(response_tree)

    def standardize_address(self, **address_components):
        # type: (**typing.Dict[str, typing.AnyStr]) -> models.Address
        [standardized] = self.standardize_addresses(
            [models.Address(**address_components)]
        )
        return standardized

    def lookup_zip_code(self):
        raise NotImplementedError

    def lookup_cities(self, zip_codes):
        # type: (typing.Iterable[str]) -> typing.Iterable[typing.Optional[models.ZipCode]]
        for idx, zip_group in enumerate(grouper(zip_codes)):
            request_element = etree.Element("CityStateLookupRequest")
            for zip_code in zip_group:
                zip_element = models.ZipCode(zip5=zip_code).xml()
                request_element.append(zip_element)
                zip_element.set("ID", "{}".format(idx))
            response_document = self.request(
                "CityStateLookup", etree.ElementTree(request_element)
            )
            for result_element in response_document.getroot():
                error_num_element = result_element.find("./Error/Number")
                if (
                    error_num_element is not None
                    and error_num_element.text == "-2147219399"
                ):
                    yield None
                    continue
                if result_element.find("./Error") is not None:
                    raise APIException(result_element)
                yield models.ZipCode.from_xml(result_element)

    def lookup_city(self, zip_code):
        # type: (str) -> typing.Optional[models.ZipCode]
        [result] = self.lookup_cities([zip_code])
        return result
