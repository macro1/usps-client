import io
import itertools
import logging

import certifi
import urllib3

try:
    import typing
except ImportError:
    pass

try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree  # type: ignore
    except ImportError:
        import xml.etree.ElementTree as etree  # type: ignore

logger = logging.getLogger()


def add_sub_element(parent, name, text):
    element = etree.SubElement(parent, name)
    element.text = text
    return element


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
        for address_group in grouper(addresses):
            request_element = etree.Element("AddressValidateRequest")
            for address_id, raw_address in enumerate(address_group):
                address_element = etree.SubElement(request_element, "Address")
                address_element.set("ID", "{}".format(address_id))
                add_sub_element(
                    address_element, "FirmName", raw_address.get("firm_name", "")
                )
                add_sub_element(
                    address_element, "Address1", raw_address.get("address", "")
                )
                add_sub_element(
                    address_element, "Address2", raw_address.get("address_2", "")
                )
                add_sub_element(address_element, "City", raw_address.get("city", ""))
                add_sub_element(address_element, "State", raw_address.get("state", ""))
                add_sub_element(address_element, "Zip5", raw_address.get("zip", ""))
                add_sub_element(address_element, "Zip4", "")

            response_tree = self.request(
                "Verify", etree.ElementTree(request_element)
            ).getroot()

            if response_tree.tag == "AddressValidateResponse":
                for address_result in response_tree:
                    address = {element.tag: element.text for element in address_result}
                    return_text = address.pop("ReturnText", None)
                    if return_text:
                        logger.warning(return_text)
                    print(address)
                    yield address
            else:
                raise APIException(response_tree)

    def standardize_address(
        self, firm_name="", address="", address_2="", city="", state="", zip=""
    ):
        [standardized] = self.standardize_addresses(
            [
                {
                    "firm_name": firm_name,
                    "address": address,
                    "address_2": address_2,
                    "city": city,
                    "state": state,
                    "zip": zip,
                }
            ]
        )
        return standardized

    def lookup_zip_code(self):
        raise NotImplementedError

    def lookup_cities(self, zip_codes):
        # type: (typing.Iterable[str]) -> typing.Iterable[typing.Optional[dict]]
        for idx, zip_group in enumerate(grouper(zip_codes)):
            request_element = etree.Element("CityStateLookupRequest")
            for zip_code in zip_group:
                zip_element = etree.SubElement(request_element, "ZipCode")
                zip_element.set("ID", "{}".format(idx))
                zip5_element = etree.SubElement(zip_element, "Zip5")
                zip5_element.text = zip_code
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
                yield {e.tag: e.text for e in result_element}

    def lookup_city(self, zip_code):
        # type: (str) -> typing.Optional[dict]
        [result] = self.lookup_cities([zip_code])
        return result
