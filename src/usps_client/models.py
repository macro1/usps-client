from typing import Text, TypeVar

from attr import define, field

from .base_model import Base

try:
    T = TypeVar("T", bound="Base")
except AttributeError:
    pass


@define
class RequestAddress(Base):
    TAG = "Address"
    firm_name: Text | None = ""
    address1: Text | None = ""
    address2: Text | None = ""
    city: Text | None = ""
    state: Text | None = ""
    zip5: Text | None = ""
    zip4: Text | None = ""


@define
class ResponseAddress(Base):
    TAG = "Address"
    firm_name: Text | None = ""
    address1: Text | None = ""
    address2: Text | None = ""
    city: Text | None = ""
    city_abbreviation: Text | None = ""
    state: Text | None = ""
    zip5: Text | None = ""
    zip4: Text | None = ""
    return_text: Text | None = ""
    delivery_point: Text | None = ""
    carrier_route: Text | None = ""
    footnotes: Text | None = ""
    dpv_confirmation: Text | None = ""
    dpvcmra: Text | None = ""
    dpv_footnotes: Text | None = ""
    dpv_false: Text | None = ""
    business: Text | None = ""
    central_delivery_point: Text | None = ""
    vacant: Text | None = ""


@define
class ZipCode(Base):
    TAG = "ZipCode"
    zip5: Text | None = ""
    city: Text | None = ""
    state: Text | None = ""
    financenumber: Text | None = ""
    classificationcode: Text | None = ""


@define
class SpecialService(Base):
    TAG = "SpecialService"
    service_id: Text | None = None
    service_name: Text | None = None
    available: Text | None = None
    price: Text | None = None
    declared_value_required: Text | None = None
    due_sender_required: Text | None = None


@define
class Postage(Base):
    TAG = "Postage"
    mail_service: Text | None = None
    rate: Text | None = None
    special_services: list[SpecialService] = field(
        factory=list, metadata={"model": SpecialService}
    )


@define
class RequestPackage(Base):
    TAG = "Package"
    service: Text | None = None
    zip_origination: Text | None = None
    zip_destination: Text | None = None
    pounds: Text | None = None
    ounces: Text | None = None
    container: Text | None = None
    size: Text | None = None
    width: Text | None = None
    length: Text | None = None
    height: Text | None = None
    girth: Text | None = None
    machinable: Text | None = None


@define
class ResponsePackage(Base):
    TAG = "Package"
    zip_origination: Text | None = None
    zip_destination: Text | None = None
    pounds: Text | None = None
    ounces: Text | None = None
    container: Text | None = None
    size: Text | None = None
    zone: Text | None = None
    postage: Postage | None = field(default=None, metadata={"model": Postage})
