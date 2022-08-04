from typing import List, Optional, Text, TypeVar, cast

from attr import define, field

from .base_model import Base

try:
    T = TypeVar("T", bound="Base")
except AttributeError:
    pass


@define
class RequestAddress(Base):
    TAG = "Address"
    firm_name: Optional[Text] = ""
    address1: Optional[Text] = ""
    address2: Optional[Text] = ""
    city: Optional[Text] = ""
    state: Optional[Text] = ""
    zip5: Optional[Text] = ""
    zip4: Optional[Text] = ""


@define
class ResponseAddress(Base):
    TAG = "Address"
    firm_name: Optional[Text] = ""
    address1: Optional[Text] = ""
    address2: Optional[Text] = ""
    city: Optional[Text] = ""
    city_abbreviation: Optional[Text] = ""
    state: Optional[Text] = ""
    zip5: Optional[Text] = ""
    zip4: Optional[Text] = ""
    return_text: Optional[Text] = ""
    delivery_point: Optional[Text] = ""
    carrier_route: Optional[Text] = ""
    footnotes: Optional[Text] = ""
    dpv_confirmation: Optional[Text] = ""
    dpvcmra: Optional[Text] = ""
    dpv_footnotes: Optional[Text] = ""
    dpv_false: Optional[Text] = ""
    business: Optional[Text] = ""
    central_delivery_point: Optional[Text] = ""
    vacant: Optional[Text] = ""


@define
class ZipCode(Base):
    TAG = "ZipCode"
    zip5: Optional[Text] = ""
    city: Optional[Text] = ""
    state: Optional[Text] = ""
    financenumber: Optional[Text] = ""
    classificationcode: Optional[Text] = ""


@define
class SpecialService(Base):
    TAG = "SpecialService"
    service_id: Optional[Text] = None
    service_name: Optional[Text] = None
    available: Optional[Text] = None
    price: Optional[Text] = None
    declared_value_required: Optional[Text] = None
    due_sender_required: Optional[Text] = None


@define
class Postage(Base):
    TAG = "Postage"
    mail_service: Optional[Text] = None
    rate: Optional[Text] = None
    special_services: Optional[List[SpecialService]] = cast(
        Optional[List[SpecialService]],
        field(factory=list, metadata={"model": SpecialService}),
    )


@define
class RequestPackage(Base):
    TAG = "Package"
    service: Optional[Text] = None
    zip_origination: Optional[Text] = None
    zip_destination: Optional[Text] = None
    pounds: Optional[Text] = None
    ounces: Optional[Text] = None
    container: Optional[Text] = None
    size: Optional[Text] = None
    width: Optional[Text] = None
    length: Optional[Text] = None
    height: Optional[Text] = None
    girth: Optional[Text] = None
    machinable: Optional[Text] = None


@define
class ResponsePackage(Base):
    TAG = "Package"
    zip_origination: Optional[Text] = None
    zip_destination: Optional[Text] = None
    pounds: Optional[Text] = None
    ounces: Optional[Text] = None
    container: Optional[Text] = None
    size: Optional[Text] = None
    zone: Optional[Text] = None
    postage: Optional[Postage] = field(default=None, metadata={"model": Postage})
