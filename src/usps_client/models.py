import attr

import inflection

from . import etree, typing

try:
    T = typing.TypeVar("T", bound="Base")
except AttributeError:
    pass


def add_sub_element(parent, name, text):
    # type: (etree.Element, typing.Text, typing.Optional[typing.Text]) -> etree.Element
    element = etree.SubElement(parent, name)
    element.text = text or ""
    return element


class Base(object):
    TAG = ""  # type: typing.Text

    def xml(self):
        # type: () -> etree.Element
        element = etree.Element(self.TAG)
        for field in attr.fields(type(self)):
            field_name = field.name
            value = getattr(self, field_name)
            add_sub_element(
                element,
                inflection.camelize(field_name, uppercase_first_letter=True),
                value,
            )
        return element

    @classmethod
    def from_xml(cls, xml):
        # type: (typing.Type[T], etree.Element) -> typing.Optional[T]
        data = {
            inflection.underscore(element.tag): element.text
            for element in xml
            if element.tag != "ReturnText"
        }
        if not data:
            return None
        return cls(**data)  # type: ignore


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
