import requests, urllib3

USERNAME = 'root'
PASSWORD = 'laboratory'

API_URL = 'https://labisilon-mgr.rede.tst:8080/platform'

API_CALLS = {
    'groupnets': '/3/network/groupnets',
    'subnets': '/3/network/groupnets/%s/subnets',
    'pools': '/3/network/groupnets/%s/subnets/%s/pools',
    'rules': '/3/network/groupnets/%s/subnets/%s/pools/%s/rules',
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IsiJson(object):

    def __init__(self, json_attribute_name, api_call_template, parents={}, children=[]):
        self.json_attribute_name = json_attribute_name
        self.api_call_template = api_call_template
        self.parents = parents
        self.children = children
        
        self.objects = []

    def get_object(self):
        response = requests.get(self.get_api_call_string(), auth=('root', 'laboratory'), verify=False)

        if response.status_code == 200:
            data = response.json()

            self.objects = data[self.json_attribute_name]

        else: 
            print('deu merda')

    def get_api_call_string(self):
        return self.api_call_template

class Groupnets(IsiJson):

    def __init__(self):
        super().__init__('groupnets', API_CALLS['groupnets'], {}, ['subnets'])

    def get_api_call_string(self):
        return API_URL + ( API_CALLS[self.json_attribute_name])


if __name__ == "__main__":

    groupnets = Groupnets()

    groupnets.get_object()    