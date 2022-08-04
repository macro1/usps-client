import re
from html import unescape
from typing import TYPE_CHECKING

import attr
import inflection

from .shims import etree

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Type, TypeVar, Union

    from .shims import Element

    T = TypeVar("T", bound="Base")


def add_sub_element(parent: "Element", name: str, text: "Optional[str]") -> "Element":
    element: Element = etree.SubElement(parent, name)
    if text is not None:
        element.text = text
    return element


def deserialize_value(
    element: "Element", field: "Optional[attr.Attribute[Any]]" = None
) -> "Any":
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
    def TAG(self) -> str:
        raise NotImplementedError

    def __init__(self, **data: "Union[str, T, None]") -> None:
        super().__init__()

    def xml(self) -> "Element":
        element: Element = etree.Element(self.TAG)
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
    def from_xml(cls: "Type[T]", xml: "Element") -> "Optional[T]":
        fields = attr.fields_dict(cls)
        data: "Dict[str, Union[str, T]]" = {}
        for element in xml:
            attribute_name = inflection.underscore(element.tag)
            data[attribute_name] = deserialize_value(element, fields[attribute_name])
        if not data:
            return None
        return cls(**data)
