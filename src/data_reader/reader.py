import json


class ApiDataReader(object):
    """Get api data from json file"""

    def __init__(self, filepath):
        try:
            fp = open(filepath)
        except Exception as ex:
            print(ex)
        else:
            with fp:
                data = json.load(fp)
                self.api_key = data['api_key']
                self.api_secret = data['api_secret']
                self.api_url = data['api_url']
                fp.close()


class AppDataReader(object):
    """Get app data from json file"""

    def __init__(self, filepath):
        try:
            fp = open(filepath)
        except Exception as ex:
            print(ex)
        else:
            with fp:
                data = json.load(fp)
                self.path_saved = data['path_saved']
                fp.close()
