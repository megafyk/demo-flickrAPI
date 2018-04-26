import json
import os
import math
import re
import requests
import shutil
from data_reader.reader import ApiDataReader
from data_reader.reader import AppDataReader
from progress_bar.progress_bar import printProgressBar


def download_img(url, path_saved):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        filename = url.rsplit('/', 1)[1]
        with open(os.path.join(path_saved, filename), 'wb') as f:
            chunk_size = 128
            l = math.ceil(len(r.content)/chunk_size)
            print('+[Downloading] ' + filename)
            printProgressBar(0, l, prefix='Progress:',
                             suffix='Complete', length=50)
            for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                f.write(chunk)
                printProgressBar(i+1, l, prefix='Progress:',
                                 suffix='Complete', length=50)
            f.close()


def download_link():
    print('def download by link')


def download_links():
    print('def download by links from file')


def get_photo_id(url):
    return url.rsplit('/', 4)[1]


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)


def choose_options(num_option):
    options = {
        0: download_link,
        1: download_links,
        2: lambda: "download_none"
    }
    func = options.get(num_option, lambda: "nothing")
    return func


def print_choose_options():
    print('Please choose an option: ')
    print('1. download by link')
    print('2. download by links from file')
    option = input('Enter your option: ')
    return choose_options(option)


if __name__ == '__main__':
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
        print_choose_options()
        url = input('Enter your link: ')
        if(is_valid_url(url)):
            params['photo_id'] = get_photo_id(url)
            print('Processing...')
            r = requests.get(api_data_reader.api_url, params=params)
            if(r.status_code == 200):
                data = r.json()
                if(data['sizes']['candownload'] == 1):
                    isAutoDownload = True
                else:
                    isAutoDownload = input(
                        'Download automacally? (y/n): ') == 'y'
                if isAutoDownload:
                    download_img(data['sizes']['size'][-1]['source'],
                                 app_data_reader.path_saved)
            else:
                print('There is somethings wrong - Error code: %d' %
                      r.status_code)
        else:
            print('Wrong url...')
        isContinue = input('Do you want to continue? (y/n): ').lower() == 'y'
        if isContinue != True:
            break
