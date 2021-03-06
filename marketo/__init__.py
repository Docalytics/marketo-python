from marketo import version, auth

VERSION = version.VERSION
__version__ = VERSION

import requests

from marketo.wrapper import get_lead, get_lead_activity, request_campaign, get_campaigns_for_source, sync_lead


class Client:

    def __init__(self, soap_endpoint=None, user_id=None, encryption_key=None):

        if not soap_endpoint or not isinstance(soap_endpoint, (str, unicode)):
            raise ValueError('Must supply a soap_endpoint as a non empty string.')

        if not user_id or not isinstance(user_id, (str, unicode)):
            raise ValueError('Must supply a user_id as a non empty string.')

        if not encryption_key or not isinstance(encryption_key, str):
            raise ValueError('Must supply a encryption_key as a non empty string.')

        self.soap_endpoint = soap_endpoint
        self.user_id = user_id
        self.encryption_key = encryption_key

    def wrap(self, body):
        return (
            '<?xml version="1.0" encoding="UTF-8"?>' +
            '<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' +
                          'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' +
                          'xmlns:wsdl="http://www.marketo.com/mktows/" ' +
                          'xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" ' +
                          'xmlns:ins0="http://www.marketo.com/mktows/" ' +
                          'xmlns:ns1="http://www.marketo.com/mktows/" ' +
                          'xmlns:mkt="http://www.marketo.com/mktows/">' +
                auth.header(self.user_id, self.encryption_key) +
                '<env:Body>' +
                    body +
                '</env:Body>' +
            '</env:Envelope>')

    def request(self, body):
        envelope = self.wrap(body)
        response = requests.post(self.soap_endpoint, data=envelope,
            headers={
                'Connection': 'Keep-Alive',
                'Soapaction': '',
                'Content-Type': 'text/xml;charset=UTF-8',
                'Accept': '*/*'})
        return response

    def get_lead(self, email=None):

        if not email or not isinstance(email, (str, unicode)):
            raise ValueError('Must supply an email as a non empty string.')

        body = get_lead.wrap(email)
        response = self.request(body)
        if response.status_code == 200:
            return get_lead.unwrap(response)
        else:
            raise Exception(response.text)

    def get_lead_activity(self, email=None):

        if not email or not isinstance(email, (str, unicode)):
            raise ValueError('Must supply an email as a non empty string.')

        body = get_lead_activity.wrap(email)
        response = self.request(body)
        if response.status_code == 200:
            return get_lead_activity.unwrap(response)
        else:
            raise Exception(response.text)

    def request_campaign(self, campaignId, leadId=None, leadIdType='IDNUM', leads=None):
        """
        Adds a lead or leads to a campaign.

        :type campaignId: str
        :param campaignId: the id of the campaign to which the leads will be added

        :type leadId: str
        :param leadId: the id of a lead to be added to the campaign. Used for adding a single lead to a campaign. May
        not be used if leads is specified.

        :type leadIdType: the type of the id being passed. Defaults to 'IDNUM'. Possible values are: 'IDNUM'
        (Marketo lead id), 'COOKIE' (Munkin cookie for a lead), 'EMAIL' (email address for a lead), 'SFDCLEADID'
        (Salesforce id for a lead), 'LEADOWNEREMAIL' (the email address of the owner of the lead), 'SFDCACCOUNTID'
        (account id from Salesforce), 'SFDCCONTACTID' (the contact id from Salesforce), 'SFDCLEADID' (the lead id from
        Salesforce), 'SFDCLEADOWNERID' (the lead owner id from Salesforce), 'SFDCOPPTYID' (the opportunity id from
        Salesforce)

        :type leads: list of tuples or tuple of tuples
        :param leads: multiple leads to be added to the campaign. May not be used with the leadId parameter. For
        each individual tuple, the first value is the id of the lead, the second value is the type of the lead id. See
        leadIdType for a list of possible values.

        :returns: True on success, exception on failure
        """
        if not campaignId or not isinstance(campaignId, (str, unicode)):
            raise ValueError('Must supply campaign id as a non empty string.')

        if leadId and leads:
            raise ValueError('Cannot specify both leadId and leads')

        if leadId:
            # Single lead
            if not leadIdType:
                raise ValueError('leadIdType must be specified')

            # Convert into list
            leads = [(leadId, leadIdType)]

        for lead in leads:
            # Check lead id
            if not lead[0] or not isinstance(lead[0], (str, unicode)):
                raise ValueError('non-empty string required for lead id')

            # CHeck lead id type
            if not lead[1] or not isinstance(lead[1], (str, unicode)) or lead[1] not in ['IDNUM', 'COOKIE', 'EMAIL',
                                                                                         'SFDCLEADID', 'LEADOWNEREMAIL',
                                                                                         'SFDCACCOUNTID',
                                                                                         'SFDCCONTACTID', 'SFDCLEADID',
                                                                                         'SFDCLEADOWNERID',
                                                                                         'SFDCOPPTYID']:
                raise ValueError("'%s' is an invalid lead id type' % lead[1]")

        body = request_campaign.wrap(campaignId, leads)

        response = self.request(body)
        if response.status_code == 200:
            return True
        else:
            raise Exception(response.text)

    def get_campaigns_for_source(self, source='MKTOWS', name=None, exactName=False):
        """
        Create request body for getCampaignsForSource.

        :type source: str
        :param source: the source requested. Possible values 'MKTOWS' or 'SALES'

        :type name: str
        :param name: the name filter to apply to the request. Optional.

        :type exactName: bool
        :param exactName: boolean flag indicating if the returned campaigns must be an exact match to name
        """


        if not source or not isinstance(source, (str, unicode)):
            raise ValueError('Must supply source as a non empty string.')

        if name and not isinstance(name, (str, unicode)):
            raise ValueError('Must supply lead id as a non empty string.')

        body = get_campaigns_for_source.wrap(source, name, exactName)

        response = self.request(body)
        if response.status_code == 200:
            return get_campaigns_for_source.unwrap(response)
        else:
            raise Exception(response.text)

    def sync_lead(self,
                  email=None,
                  marketo_id=None,
                  marketo_cookie=None,
                  foreign_system_id=None,
                  foreign_system_type=None,
                  attributes=None):
        """
        Push information about a lead to Marketo. Lead must be identified by one or more of email, marketo_id,
        marketo_cookie, or foriegn_system_id. See http://developers.marketo.com/documentation/soap/synclead/ for more
        details.

        :type email: str
        :param email: the email address of the lead

        :type marketo_id: str
        :param marketo_id: the marketo generated id for a lead

        :type marketo_cookie: str
        :param marketo_cookie: a marketo cookie generated for a lead by Marketo's munchkin.js

        :type foreign_system_id: str
        :param foreign_system_id: a foriegn system identifier for a lead

        :type foreign_system_type: str
        :param foreign_system_type: the type of foreign system for foreign_system_id. Required if foreign_system_id
        is passed. Possible values are 'CUSTOM', 'SFDC', 'NETSUITE'

        :type attributes: tuple, dict
        :param attributes: the information about the lead to be pushed to marketo either in the form of tuples or a
        dictionary

        :returns: a lead object for the lead that was sync'ed
        """
        if (not email or not isinstance(email, (str, unicode))) \
                and (not marketo_id or not isinstance(marketo_id, (str, unicode))) \
                and (not marketo_cookie or not isinstance(marketo_cookie, (str, unicode))) \
                and (not foreign_system_id or not isinstance(foreign_system_id, (str, unicode))):
            raise ValueError('Must supply lead identification in email, marketo_id, '
                             'marketo_cookie, or foreign_system_id as a non empty string.')

        if foreign_system_id and not foreign_system_type:
            raise ValueError('foreign_system_type must be specified with foreign_system_id')

        if foreign_system_id and foreign_system_type and foreign_system_type not in ['CUSTOM', 'SFDC', 'NETSUITE']:
            raise ValueError('foreign_system_type must be \'CUSTOM\', \'SFDC\', or \'NETSUITE\'')

        if not attributes or (not isinstance(attributes, tuple) and not isinstance(attributes, dict)):
            raise ValueError('Must supply attributes as a non empty tuple or dict.')

        body = sync_lead.wrap(
            email=email,
            marketo_id=marketo_id,
            marketo_cookie=marketo_cookie,
            foreign_system_id=foreign_system_id,
            attributes=attributes)

        response = self.request(body)
        if response.status_code == 200:
            return sync_lead.unwrap(response)
        else:
            raise Exception(response.text)
