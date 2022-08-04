import re
from html import unescape
from typing import Any, Text, Type, TypeVar

import attr
import inflection

from .shims import etree

T = TypeVar("T", bound="Base")


def add_sub_element(
    parent: etree.Element, name: Text, text: Text | None
) -> etree.Element:
    element = etree.SubElement(parent, name)
    if text is not None:
        element.text = text
    return element


def deserialize_value(
    element: etree.Element, field: "attr.Attribute[Any] | None" = None
) -> Any:
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
    def TAG(self) -> Text:
        raise NotImplementedError

    def __init__(self, **data: str | T | None) -> None:
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
    def from_xml(cls: Type[T], xml: etree.Element) -> T | None:
        fields = attr.fields_dict(cls)
        data: dict[Text, Text | T] = {}
        for element in xml:
            attribute_name = inflection.underscore(element.tag)
            data[attribute_name] = deserialize_value(element, fields[attribute_name])
        if not data:
            return None
        return cls(**data)
