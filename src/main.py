import json
import os
import requests
import shutil
from time import sleep
from data_reader.reader import ApiDataReader
from data_reader.reader import AppDataReader
from progress_bar.progress_bar import printProgressBar


def get_photo_id(url):
    return url.rsplit('/', 4)[1]


def download_img(url, path_saved):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        filename = url.rsplit('/', 1)[1]
        with open(os.path.join(path_saved, filename), 'wb') as f:
            r.raw.decode_content = True
            l = len(r.content)
            printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            for i,chunk in r:
                f.write(chunk)
                sleep(0.1)
                # Update Progress Bar
                printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


api_data_reader = ApiDataReader(filepath=os.path.join(
    os.path.dirname(os.path.__file__), '../src/data/api_data.json'))
app_data_reader = AppDataReader(filepath=os.path.join(
    os.path.dirname(os.path.__file__), '../src/data/app_data.json'))
params = {
    'method': 'flickr.photos.getSizes',
    'api_key': api_data_reader.api_key,
    'photo_id': '',
    'format': 'json',
    'nojsoncallback': '1'
}
while True:
    url = input('Input image url: ')
    params['photo_id'] = get_photo_id(url)
    r = requests.get(api_data_reader.api_url, params=params)
    if(r.status_code == 200):
        print('Processing...')
        data = r.json()
        if(data['sizes']['candownload'] == 1):
            print('can download')
        else:
            print('cant download')
        download_img(data['sizes']['size'][-1]['source'],
                     app_data_reader.path_saved)
    else:
        print('There is somethings wrong - Error code: %d' % r.status_code)
    isContinue = input('Do you want to continue...(y/n)').lower() == 'y'
    if isContinue != True:
        break
