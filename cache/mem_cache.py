import hashlib

try:
    import simplejson as json
except ImportError:
    import json

CACHE_BOX = dict()


# memory cache , if you have enough phsical memorys.
def cache(func):
    '''
    When method/function is called, returns the cache if it exists;
    otherwise executes the method and cache results.

    Specific to make_http_request() function, because it uses 'url'
    argument to create the cache key.
    '''

    def _wrapper(*args, **kwargs):
        cache_key = hashlib.sha1(args[0].encode('utf-8')).hexdigest()

        # print('Looking for cache: %s' % args[0])

        data = CACHE_BOX.get(cache_key)
        # Check the value is cached, if cached return cached content
        if data:
            # print('Cache found: %s' % args[0])
            return json.loads(data)
        else:
            # print('Cache not found, making request: %s' % args[0])
            # Cache returned data of the caller function and finally return the data
            json_data = func(*args, **kwargs)

            CACHE_BOX[cache_key] = json.dumps(json_data)

            return json_data

    return _wrapper
