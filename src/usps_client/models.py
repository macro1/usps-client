import attr

from . import etree


def tag_to_attr(tag_name):
    return tag_name.lower()


def add_sub_element(parent, name, text):
    element = etree.SubElement(parent, name)
    element.text = text or ""
    return element


class Base(object):
    def xml(self):
        raise NotImplemented

    @classmethod
    def from_xml(cls, xml):
        data = {
            tag_to_attr(element.tag): element.text
            for element in xml
            if element.tag != "ReturnText"
        }
        if not data:
            return
        return cls(**data)


@attr.s
class Address(Base):
    firmname = attr.ib(default=None)
    address1 = attr.ib(default=None)
    address2 = attr.ib(default=None)
    city = attr.ib(default=None)
    state = attr.ib(default=None)
    zip5 = attr.ib(default=None)
    zip4 = attr.ib(default=None)

    def xml(self):
        address_element = etree.Element("Address")
        add_sub_element(address_element, "FirmName", self.firmname)
        add_sub_element(address_element, "Address1", self.address1)
        add_sub_element(address_element, "Address2", self.address2)
        add_sub_element(address_element, "City", self.city)
        add_sub_element(address_element, "State", self.state)
        add_sub_element(address_element, "Zip5", self.zip5)
        add_sub_element(address_element, "Zip4", self.zip4)
        return address_element

    @classmethod
    def from_xml(cls, xml):
        address = {
            tag_to_attr(element.tag): element.text
            for element in xml
            if element.tag != "ReturnText"
        }
        if not address:
            return
        return cls(**address)


@attr.s
class ZipCode(Base):
    zip5 = attr.ib(default=None)
    city = attr.ib(default=None)
    state = attr.ib(default=None)
    financenumber = attr.ib(default=None)
    classificationcode = attr.ib(default=None)

    def xml(self):
        zipcode_element = etree.Element("ZipCode")
        add_sub_element(zipcode_element, "Zip5", self.zip5)
        add_sub_element(zipcode_element, "City", self.city)
        add_sub_element(zipcode_element, "State", self.state)
        add_sub_element(zipcode_element, "FinanceNumber", self.financenumber)
        add_sub_element(zipcode_element, "ClassificationCode", self.classificationcode)
        return zipcode_element
