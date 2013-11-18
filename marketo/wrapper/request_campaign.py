from xml.sax.saxutils import escape

def wrap(campaignId, leads, source='MKTOWS'):
    leadList = ''
    for lead in leads:
        leadList += '<leadKey>' + \
                    '<keyValue>' + escape(lead[0]) + '</keyValue>' + \
                    '<keyType>' + escape(lead[1]) + '</keyType>' + \
                    '</leadKey>'

    return (
        '<mkt:paramsRequestCampaign>' +
            '<source>' + escape(source) + '</source>' +
            '<campaignId>' + escape(campaignId) + '</campaignId>' +
            '<leadList>' + leadList + '</leadList>' +
        '</mkt:paramsRequestCampaign>')
