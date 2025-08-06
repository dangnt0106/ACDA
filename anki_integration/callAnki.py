import urllib.request
import json

class callAnki:
    def __init__(self, deck_name):
        self.deck_name = deck_name

    def request2(self, action, **params):
        return {'action': action, 'params': params, 'version': 6}

    def invoke(self, action, **params):
        requestJson = json.dumps(self.request2(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(
            urllib.request.Request('http://127.0.0.1:8765', data=requestJson)
        ))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']
