import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from marketo.wrapper import campaign_record

def wrap(source='MKTOWS', name=None, exactName=False):
    """
    Create request body for getCampaignsForSource.

    :type source: str
    :param source: the source requested. Possible values 'MKTOWS' or 'SALES'

    :type name: str
    :param name: the name filter to apply to the request. Optional.

    :type exactName: bool
    :param exactName: boolean flag indicating if the returned campaigns must be an exact match to name

    :returns: string of XML for the request body
    """
    nameRestriction = ''
    if name:
        nameRestriction = '<name>' + escape(name) + '</name>' + \
                          '<exactName>' + ('true' if exactName else 'false') + '</exactName>'

    return (
        '<mkt:paramsGetCampaignsForSource>' +
            '<source>' + escape(source) + '</source>' +
            nameRestriction +
        '</mkt:paramsGetCampaignsForSource>')


def unwrap(response):
    """
    Unwrap a getCampaignsForSource response.

    :type response: requests module HTTP response
    :param response: response from the SOAP request

    :returns; list of campaigns
    """
    root = ET.fromstring(response.text)
    campaigns = []

    for child in root.find('.//campaignRecordList'):
        campaigns.append(campaign_record.unwrap(child))

    return campaigns