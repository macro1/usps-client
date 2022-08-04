from types import ModuleType
from typing import Type, TypeVar

etree: ModuleType
try:
    from lxml import etree as lxml_etree
except ImportError:
    try:
        from xml.etree import cElementTree as stdlib_cElementTree
    except ImportError:
        from xml.etree import ElementTree as stdlib_ElementTree

        etree = stdlib_ElementTree
    else:
        etree = stdlib_cElementTree
else:
    etree = lxml_etree

Element = TypeVar(
    "Element",
    lxml_etree._Element,
    stdlib_cElementTree.Element,
    stdlib_ElementTree.Element,
)
ElementTree = TypeVar(
    "ElementTree",
    lxml_etree._ElementTree,
    stdlib_cElementTree.ElementTree,
    stdlib_ElementTree.ElementTree,
)
