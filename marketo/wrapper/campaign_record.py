

class CampaignRecord:

    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return "Campaign (%s - %s)" % (self.id, self.name)

    def __repr__(self):
        return self.__str__()


def unwrap(xml):
    campaign = CampaignRecord()
    campaign.id = xml.find('id').text
    campaign.name = xml.find('name').text
    campaign.description = xml.find('description').text

    return campaign
