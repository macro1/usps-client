import attr

from .base_model import Base
from .shims import typing


@attr.s(slots=True)
class Address(Base):
    TAG = "Address"
    firm_name = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    address1 = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    address2 = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    city = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    state = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    zip5 = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    zip4 = attr.ib(default=None)  # type: typing.Optional[typing.Text]


@attr.s(slots=True)
class ZipCode(Base):
    TAG = "ZipCode"
    zip5 = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    city = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    state = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    financenumber = attr.ib(default=None)  # type: typing.Optional[typing.Text]
    classificationcode = attr.ib(default=None)  # type: typing.Optional[typing.Text]
