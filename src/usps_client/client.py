import io
import itertools
import logging

import certifi
import urllib3

from . import etree, models, typing

try:
    T = typing.TypeVar("T")
    M = typing.TypeVar("M", bound=models.Base)
except AttributeError:
    pass

logger = logging.getLogger()


def grouper(iterable):
    # type: (typing.Iterable[T]) -> typing.Generator[typing.List[T], None, None]
    iterable = iter(iterable)

    def just_five(iterable):
        # type: (typing.Iterable[T]) -> typing.List[T]
        return list(itertools.islice(iterable, 5))

    while True:
        next_group = just_five(iterable)
        if not next_group:
            return
        yield next_group


class APIException(Exception):
    def __init__(self, element):
        # type: (etree.Element) -> None
        if not isinstance(element, type(etree.ElementTree())):
            element = etree.ElementTree(element)
        xml_buffer = io.BytesIO()
        element.write(xml_buffer)
        super(APIException, self).__init__(xml_buffer.getvalue())


class Client:
    BASE_URL = "https://secure.shippingapis.com/ShippingAPI.dll"
    ENCODING = "iso-8859-1"

    def __init__(self, user_id, pool_manager=None):
        # type: (typing.Text, typing.Optional[urllib3.PoolManager]) -> None
        self.user_id = user_id
        if pool_manager is None:
            self.pool_manager = urllib3.PoolManager(
                headers={"User-Agent": "usps-client"},
                cert_reqs="CERT_REQUIRED",
                ca_certs=certifi.where(),
            )
        else:
            self.pool_manager = pool_manager

    def request(self, api, element_tree):
        # type: (typing.Text, etree.ElementTree) -> etree.ElementTree
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

    def query_list(self, api, model, iterable, wrapping_element=None):
        # type: (typing.Text, typing.Type[M], typing.Iterable[M], typing.Optional[typing.Text]) -> typing.Iterable[typing.Optional[M]]
        if wrapping_element is None:
            wrapping_element = api
        request_element_name = "{}Request".format(wrapping_element)
        response_element_name = "{}Response".format(wrapping_element)
        for request_group in grouper(iterable):
            request_element = etree.Element(request_element_name)
            for item_id, item_data in enumerate(request_group):
                item_element = item_data.xml()
                item_element.set("ID", "{}".format(item_id))
                request_element.append(item_element)

            response_tree = self.request(
                api, etree.ElementTree(request_element)
            ).getroot()

            if response_tree.tag != response_element_name:
                raise APIException(response_tree)
            for result_element in response_tree:
                error_number_element = result_element.find("./Error/Number")
                if error_number_element is not None:
                    if (
                        error_number_element.text == "-2147219399"
                    ):  # No result for zipcode (such as '00000')
                        yield None
                    else:
                        raise APIException(result_element)
                else:
                    yield model.from_xml(result_element)

    def query_single(self, api, model, data, wrapping_element=None):
        # type: (typing.Text, typing.Type[M], typing.Dict[typing.Text, typing.Optional[typing.Text]], typing.Optional[typing.Text]) -> typing.Optional[M]
        [result] = self.query_list(api, model, [model(**data)], wrapping_element)
        return result

    def standardize_addresses(self, addresses):
        # type: (typing.Iterable[models.Address]) -> typing.Iterable[typing.Optional[models.Address]]
        return self.query_list(
            "Verify", models.Address, addresses, wrapping_element="AddressValidate"
        )

    def standardize_address(self, **address_components):
        # type: (typing.Optional[typing.Text]) -> typing.Optional[models.Address]
        return self.query_single(
            "Verify",
            models.Address,
            address_components,
            wrapping_element="AddressValidate",
        )

    def lookup_zip_codes(self, addresses):
        # type: (typing.Iterable[models.Address]) -> typing.Iterable[typing.Optional[models.Address]]
        return self.query_list("ZipCodeLookup", models.Address, addresses)

    def lookup_zip_code(self, **address_components):
        # type: (typing.Optional[typing.Text]) -> typing.Optional[models.Address]
        return self.query_single("ZipCodeLookup", models.Address, address_components)

    def lookup_cities(self, zip_codes):
        # type: (typing.Iterable[typing.Text]) -> typing.Iterable[typing.Optional[models.ZipCode]]
        return self.query_list(
            "CityStateLookup",
            models.ZipCode,
            (models.ZipCode(zip5=zip_code) for zip_code in zip_codes),
        )

    def lookup_city(self, zip_code):
        # type: (typing.Text) -> typing.Optional[models.ZipCode]
        return self.query_single("CityStateLookup", models.ZipCode, {"zip5": zip_code})
