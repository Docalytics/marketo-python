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
    attr = ''
    for i in attributes:
        attr += '<attribute>' \
            '<attrName>' + escape(i[0]) + '</attrName>' \
            '<attrType>' + escape(i[1]) + '</attrType>' \
            '<attrValue>' + escape(i[2]) + '</attrValue>' \
            '</attribute>'

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
        '<leadAttributeList>' + attr + '</leadAttributeList>' +
        '</leadRecord>' +
        '<returnLead>true</returnLead>' +
        '</mkt:paramsSyncLead>'
    )


def unwrap(response):
    root = ET.fromstring(response.text)
    lead_record_xml = root.find('.//leadRecord')
    return lead_record.unwrap(lead_record_xml)
