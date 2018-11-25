import json
import os
import math
import pathlib
import re
import requests
import shutil
from colorama import init, Fore
from enum import Enum

from clipboard_writer.writer import ClipboardWriter
from data_reader.reader import ApiDataReader
from data_reader.reader import AppDataReader
from progress_bar.progress_bar import printProgressBar


class Option(Enum):
    DOWNLOAD_LINK = 0
    DOWNLOAD_LINKS = 1


def download_img(url, path_saved):
    """Download image from chunk.

    Parameters
    ----------
    url : str
        Image url.
    path_saved : str
        Directory where to save image file.

    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        filename = url.rsplit('/', 1)[1]
        with open(os.path.join(path_saved, filename), 'wb') as f:
            chunk_size = 128
            l = math.ceil(len(r.content)/chunk_size)
            print(Fore.LIGHTBLUE_EX + '[Downloading] ' + filename)
            printProgressBar(0, l, prefix='Progress:',
                             suffix='Complete', length=50)
            for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                f.write(chunk)
                printProgressBar(i+1, l, prefix='Progress:',
                                 suffix='Complete', length=50)
            f.close()


def download_link():
    """Set one image url to chunk.

    """
    url = input('Enter your link: ')
    if(is_valid_url(url)):
        urls_dict[get_author_id(url)] = [url]
    else:
        print(Fore.RED + 'Wrong url...')
        pass


def download_links():
    """Set multiple download url to chunk.

    """
    file_path = input('Enter your file path: ')
    p = pathlib.Path(file_path)
    if p.is_file():
        with open(p) as f:
            lines = f.readlines()
            for i, url in enumerate(lines):
                url = url.rstrip()
                if is_valid_url(url):
                    author_id = get_author_id(url)
                    if author_id in urls_dict:
                        if url in urls_dict[author_id]:
                            print(Fore.YELLOW + 'Duplicate url in lines: %d' % i)
                        else:
                            urls_dict[author_id].append(url)
                    else:
                        urls_dict[author_id] = [url]
                else:
                    print(Fore.RED + 'Wrong url in line: %d' % i)
        f.close()
    else:
        print(Fore.RED + 'Wrong file path.')


def write_url():
    """  """
    file_path = input('Enter your file path: ')
    p = pathlib.Path(file_path)
    if p.is_file():
        writer = ClipboardWriter(file_path)
        writer.run()
    else:
        print(Fore.RED + 'Wrong file path.')
    return


def get_author_id(url):
    """Get flick author id from url.

    Parameters
    ----------
    url : str
        Image url.

    Returns
    -------
    str
        Flick author id
    """
    regex = re.compile(r'(photos)(\/)([a-zA-Z0-9]+([@_ -]?[a-zA-Z0-9])*)(\/)')
    return regex.search(url).group(3)


def get_author_info(url):
    """Get flick author info from url.

    Parameters
    ----------
    url : str
        Image url.

    Returns
    -------
    json
        Flick author info.

    """
    params = {
        'method': 'flickr.urls.lookupUser',
        'api_key': api_data_reader.api_key,
        'url': url,
        'format': 'json',
        'nojsoncallback': '1'
    }
    return requests.get(api_data_reader.api_url, params=params).json()


def get_photo_id(url):
    """Get flick photo id from url.

    Parameters
    ----------
    url : str
        Image url.

    Returns
    -------
    json
        Flick photo id.

    """
    regex = re.compile(r'(\/)(\d+)(\/)')
    return regex.search(url).group(2)


def is_valid_url(url):
    """Validate url.

    Parameters
    ----------
    url : str
        Image url.

    Returns
    -------
    bool
        True if url is valid, False otherwise.

    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://# domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)


def choose_options(num_option):
    """Select feature when start app.

    Parameters
    ----------
    num_options : int
        0 is download an image
        1 is download multiple images from file 
        2 is write url to file from clipboard
    Returns
    -------
    func:
        Function selected.

    """
    options = {
        0: download_link,
        1: download_links,
        2: write_url,
        3: lambda: "download_none"
    }
    func = options.get(num_option, lambda: "nothing")
    return func()


def print_choose_options():
    """Get input selection feature from user.

    """
    print('Please choose an option: ')
    print('0. download by link')
    print('1. download by links from file')
    print('2. write clipboard url to file')
    option = input('Enter your option: ')
    choose_options(int(option))


if __name__ == '__main__':
    init(autoreset=True)
    api_data_reader = ApiDataReader(filepath='data/api_data.json')
    app_data_reader = AppDataReader(filepath='data/app_data.json')
    params = {
        'method': 'flickr.photos.getSizes',
        'api_key': api_data_reader.api_key,
        'photo_id': '',
        'format': 'json',
        'nojsoncallback': '1'
    }
    while True:
        urls_dict = {}
        try:
            print_choose_options()
        except Exception as ex:
            print(Fore.RED + str(ex))
        else:
            # Download
            print('Processing...')
            num_urls_auto = sum(len(v) for v in urls_dict.values())
            num_urls_not_auto = num_urls_success = 0
            try:
                for key in urls_dict:
                    url_temp = next(iter(urls_dict[key]))
                    params['photo_id'] = get_photo_id(url_temp)
                    r_temp = requests.get(api_data_reader.api_url, params=params)
                    data_temp = r_temp.json()
                    if(data_temp['stat'] == 'fail'):
                        print(Fore.RED + 'Error url %s' % url_temp)
                        continue
                    user_temp = get_author_info(url_temp)
                    if data_temp['sizes']['candownload'] == 1:
                        isAutoDownload = True
                    else:
                        isAutoDownload = input(
                            'Set download automacally images for %s? (y/n): ' % user_temp['user']['username']['_content']) == 'y'
                    if isAutoDownload:
                        print(Fore.LIGHTMAGENTA_EX +
                            user_temp['user']['username']['_content'])
                        for url in urls_dict[key]:
                            params['photo_id'] = get_photo_id(url)
                            r = requests.get(
                                api_data_reader.api_url, params=params)
                            data = r.json()
                            if(data['stat'] == 'fail'):
                                print(Fore.RED + 'Error url %s' % url)
                                continue
                            if r.status_code == 200 and ('sizes' in r.json()):
                                try:
                                    download_img(data['sizes']['size'][-1]['source'],
                                                app_data_reader.path_saved)
                                    num_urls_success += 1
                                except Exception as e:
                                    print(Fore.RED + str(e))
                            else:
                                print(Fore.RED + 'There is somethings wrong - Error code: %d' %
                                    data['code'])
                    else:
                        num_urls_not_auto += len(urls_dict[key])
                        num_urls_auto -= len(urls_dict[key])
                        pass
            except KeyboardInterrupt:
                pass
            print(Fore.CYAN + 'urls automatically: %d' % num_urls_auto)
            print(Fore.YELLOW + 'urls not automatically: %d' %
                  num_urls_not_auto)
            print(Fore.GREEN + 'urls success: %d' % num_urls_success)
        isContinue = input('Do you want to continue? (y/n): ').lower() == 'y'
        if isContinue != True:
            break
