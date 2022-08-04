from types import ModuleType
from typing import Any, BinaryIO, Iterable, Mapping, Optional, Protocol, Sized, Union

etree: ModuleType
try:
    from lxml import etree
except ImportError:
    try:
        from xml.etree import cElementTree as etree
    except ImportError:
        from xml.etree import ElementTree as etree


class Element(Protocol, Sized, Iterable["Element"]):
    tag: str
    # attrib
    text: str

    def find(
        self, path: str, namespaces: Optional[Mapping[str, str]] = None
    ) -> Optional["Element"]:
        ...

    def set(self, key: str, value: str) -> None:
        ...


class ElementTree(Protocol):
    def getroot(self) -> Element:
        ...

    def parse(self, source: Union[str, BinaryIO], parser: Any = None) -> Element:
        ...

    def write(
        self,
        file_or_filename: Union[str, BinaryIO],
        encoding: Optional[str] = None,
        xml_declaration: Optional[bool] = None,
        default_namespace: Optional[str] = None,
        method: Optional[str] = None,
        *,
        short_empty_elements: bool = True
    ) -> None:
        ...
