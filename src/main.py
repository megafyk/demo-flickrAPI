import json


class ApiKeys(object):
    """Get api keys from json file"""

    def __init__(self, filepath):
        try:
            fp = open(filepath)
        except Exception as ex:
            print(ex)
        else:
            with fp:
                data = json.load(fp)
                self.api_key = data['apiKey']
                self.api_secret = data['apiSecret']
                fp.close()


class TokenKeys(object):
    """Get token keys from json file"""

    def __init__(self, filepath):
        try:
            fp = open(filepath)
        except Exception as ex:
            print(ex)
        else:
            with fp:
                data = json.load(fp)
                self.token = data['token']
                self.secret = data['secret']
                fp.close()


class FlickrApi(object):
    """Flickr Api call"""

    def __init__(self, nojsoncallback=True, format='json', parameters=None):
        apiKeys = ApiKeys('secret-data/apiKeys.json')
        tokenKeys = TokenKeys('secret-data/tokenKeys.json')


flickrApi = FlickrApi()
