import re
import typing
from html import unescape

import attr
import inflection

from .shims import etree

T = typing.TypeVar("T", bound="Base")


def add_sub_element(
    parent: etree.Element, name: typing.Text, text: typing.Optional[typing.Text]
) -> etree.Element:
    element = etree.SubElement(parent, name)
    if text is not None:
        element.text = text
    return element


def deserialize_value(
    element: etree.Element, field: typing.Optional["attr.Attribute[typing.Any]"] = None
) -> typing.Any:
    if len(element):
        if field is not None:
            try:
                model = field.metadata["model"]
            except KeyError:
                pass
            else:
                if element.tag == model.TAG:
                    return model.from_xml(element)
                else:
                    return [deserialize_value(e, field) for e in element]
        return [deserialize_value(e) for e in element]
    return (
        re.sub("<[^<]+?>", "", unescape(element.text)) if element.text else element.text
    )


class Base(object):
    @property
    def TAG(self) -> typing.Text:
        raise NotImplementedError

    def __init__(self, **data: typing.Union[str, T, None]) -> None:
        super().__init__()

    def xml(self) -> etree.Element:
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
    def from_xml(cls: typing.Type[T], xml: etree.Element) -> typing.Optional[T]:
        fields = attr.fields_dict(cls)
        data = {}  # type: typing.Dict[typing.Text, typing.Union[typing.Text, T]]
        for element in xml:
            attribute_name = inflection.underscore(element.tag)
            data[attribute_name] = deserialize_value(element, fields[attribute_name])
        if not data:
            return None
        return cls(**data)
