import sys

import requests

from cache.mem_cache import cache


# from cache.file_cache import cache


@cache
def make_http_request(url):
    '''
    Makes and http request to the 'url', if response to that
    'url' is not cached yet.

    Returns the response in json format.
    '''
    request = requests.get(url)
    try:
        data = request.json()
    except ValueError:
        print("response not valid json data!")
        sys.exit()

    return data
