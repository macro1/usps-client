import typing

import attr

from .base_model import Base

try:
    T = typing.TypeVar("T", bound="Base")
except AttributeError:
    pass


@attr.s(slots=True)
class RequestAddress(Base):
    TAG = "Address"
    firm_name: typing.Optional[typing.Text] = attr.ib(default="")
    address1: typing.Optional[typing.Text] = attr.ib(default="")
    address2: typing.Optional[typing.Text] = attr.ib(default="")
    city: typing.Optional[typing.Text] = attr.ib(default="")
    state: typing.Optional[typing.Text] = attr.ib(default="")
    zip5: typing.Optional[typing.Text] = attr.ib(default="")
    zip4: typing.Optional[typing.Text] = attr.ib(default="")


@attr.s(slots=True)
class ResponseAddress(Base):
    TAG = "Address"
    firm_name: typing.Optional[typing.Text] = attr.ib(default="")
    address1: typing.Optional[typing.Text] = attr.ib(default="")
    address2: typing.Optional[typing.Text] = attr.ib(default="")
    city: typing.Optional[typing.Text] = attr.ib(default="")
    city_abbreviation: typing.Optional[typing.Text] = attr.ib(default="")
    state: typing.Optional[typing.Text] = attr.ib(default="")
    zip5: typing.Optional[typing.Text] = attr.ib(default="")
    zip4: typing.Optional[typing.Text] = attr.ib(default="")
    return_text: typing.Optional[typing.Text] = attr.ib(default="")
    delivery_point: typing.Optional[typing.Text] = attr.ib(default="")
    carrier_route: typing.Optional[typing.Text] = attr.ib(default="")
    footnotes: typing.Optional[typing.Text] = attr.ib(default="")
    dpv_confirmation: typing.Optional[typing.Text] = attr.ib(default="")
    dpvcmra: typing.Optional[typing.Text] = attr.ib(default="")
    dpv_footnotes: typing.Optional[typing.Text] = attr.ib(default="")
    dpv_false: typing.Optional[typing.Text] = attr.ib(default="")
    business: typing.Optional[typing.Text] = attr.ib(default="")
    central_delivery_point: typing.Optional[typing.Text] = attr.ib(default="")
    vacant: typing.Optional[typing.Text] = attr.ib(default="")


@attr.s(slots=True)
class ZipCode(Base):
    TAG = "ZipCode"
    zip5: typing.Optional[typing.Text] = attr.ib(default="")
    city: typing.Optional[typing.Text] = attr.ib(default="")
    state: typing.Optional[typing.Text] = attr.ib(default="")
    financenumber: typing.Optional[typing.Text] = attr.ib(default="")
    classificationcode: typing.Optional[typing.Text] = attr.ib(default="")


@attr.s(slots=True)
class SpecialService(Base):
    TAG = "SpecialService"
    service_id: typing.Optional[typing.Text] = attr.ib(default=None)
    service_name: typing.Optional[typing.Text] = attr.ib(default=None)
    available: typing.Optional[typing.Text] = attr.ib(default=None)
    price: typing.Optional[typing.Text] = attr.ib(default=None)
    declared_value_required: typing.Optional[typing.Text] = attr.ib(default=None)
    due_sender_required: typing.Optional[typing.Text] = attr.ib(default=None)


@attr.s(slots=True)
class Postage(Base):
    TAG = "Postage"
    mail_service: typing.Optional[typing.Text] = attr.ib(default=None)
    rate: typing.Optional[typing.Text] = attr.ib(default=None)
    special_services: typing.List[SpecialService] = attr.ib(
        factory=list, metadata={"model": SpecialService}
    )


@attr.s(slots=True)
class RequestPackage(Base):
    TAG = "Package"
    service: typing.Optional[typing.Text] = attr.ib(default=None)
    zip_origination: typing.Optional[typing.Text] = attr.ib(default=None)
    zip_destination: typing.Optional[typing.Text] = attr.ib(default=None)
    pounds: typing.Optional[typing.Text] = attr.ib(default=None)
    ounces: typing.Optional[typing.Text] = attr.ib(default=None)
    container: typing.Optional[typing.Text] = attr.ib(default=None)
    size: typing.Optional[typing.Text] = attr.ib(default=None)
    width: typing.Optional[typing.Text] = attr.ib(default=None)
    length: typing.Optional[typing.Text] = attr.ib(default=None)
    height: typing.Optional[typing.Text] = attr.ib(default=None)
    girth: typing.Optional[typing.Text] = attr.ib(default=None)
    machinable: typing.Optional[typing.Text] = attr.ib(default=None)


@attr.s(slots=True)
class ResponsePackage(Base):
    TAG = "Package"
    zip_origination: typing.Optional[typing.Text] = attr.ib(default=None)
    zip_destination: typing.Optional[typing.Text] = attr.ib(default=None)
    pounds: typing.Optional[typing.Text] = attr.ib(default=None)
    ounces: typing.Optional[typing.Text] = attr.ib(default=None)
    container: typing.Optional[typing.Text] = attr.ib(default=None)
    size: typing.Optional[typing.Text] = attr.ib(default=None)
    zone: typing.Optional[typing.Text] = attr.ib(default=None)
    postage: typing.Optional[Postage] = attr.ib(
        default=None, metadata={"model": Postage}
    )
