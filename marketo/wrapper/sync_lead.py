import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import lead_record


def wrap(
        email=None,
        marketo_id=None,
        marketo_cookie=None,
        foreign_system_id=None,
        foreign_system_type=None,
        attributes=None):

    email_element = '<Email>' + escape(email) + '</Email>' if email else ''
    marketo_id_element = '<Id>' + escape(marketo_id) + '</Id>' if marketo_id else ''
    marketo_cookie_element = '<marketoCookie>' + escape(marketo_cookie) + '</marketoCookie>' if marketo_cookie else ''
    foreign_system_id_element = \
        '<ForeignSysPersonId>' + escape(foreign_system_id) + '</ForeignSysPersonId>' +\
        '<ForeignSysType>' + escape(foreign_system_type) + '</ForeignSysType>' \
        if foreign_system_id and foreign_system_type else ''

    return(
        '<mkt:paramsSyncLead>' +
        marketo_cookie_element +
        '<leadRecord>' +
        email_element +
        marketo_id_element +
        foreign_system_id_element +
        '<leadAttributeList>' +
        (attributes_for_tuple(attributes) if isinstance(attributes, tuple) else attributes_for_dict(attributes)) +
        '</leadAttributeList>' +
        '</leadRecord>' +
        '<returnLead>true</returnLead>' +
        '</mkt:paramsSyncLead>'
    )


def attributes_for_dict(attributes):
    attr = ''
    for key in attributes:
        attr += '<attribute>' \
            '<attrName>' + escape(key) + '</attrName>' \
            '<attrValue>' + escape(attributes[key]) + '</attrValue>' \
            '</attribute>'

    return attr


def attributes_for_tuple(attributes):
    attr = ''
    for i in attributes:
        attrName = None
        attrType = None
        attrValue = None

        if len(i) == 2:
            attrName = i[0]
            attrValue = i[1]
        elif len(i) == 3:
            attrName = i[0]
            attrType = i[1]
            attrValue = i[2]
        else:
            raise ValueError("Invalid attribute tuple. Attribute tuples must be of the form name, value or name, type, value.")

        if attrType:
            attr += '<attribute>' \
                '<attrName>' + escape(attrName) + '</attrName>' \
                '<attrType>' + escape(attrType) + '</attrType>' \
                '<attrValue>' + escape(attrValue) + '</attrValue>' \
                '</attribute>'
        else:
            attr += '<attribute>' \
                '<attrName>' + escape(attrName) + '</attrName>' \
                '<attrValue>' + escape(attrValue) + '</attrValue>' \
                '</attribute>'

    return attr

def unwrap(response):
    root = ET.fromstring(response.text)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
