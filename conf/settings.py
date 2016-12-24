# These URLs basically points to MIT's conceptnet5 setup for Web API
BASE_LOOKUP_URL = 'http://api.conceptnet.io/'
BASE_SEARCH_URL = 'http://api.conceptnet.io/query'
BASE_ASSOCIATION_URL = 'http://api.conceptnet.io/related'

# if build locall ,use those
# BASE_LOOKUP_URL = 'http://127.0.0.1:8084/'
# BASE_SEARCH_URL = 'http://127.0.0.1:8084/query'
# BASE_ASSOCIATION_URL = 'http://127.0.0.1:8084/related'

# This is the supported query arguments for LookUp API
# :param offset: skip the specified amount of first results
# :type offset: integer
# :param limit: change the number of results from the default of 50
# :type limit: integer

SUPPORTED_LOOKUP_ARGS = ['offset', 'grouped', 'limit']

# This is the supported query arguments for Association API
# :param limit: change the number of results from the default of 50
# :type limit: integer
# :param filter: return only results that start with the given URI. For example, 
#                filter=/c/en returns results in English.
# :type filter: a uri, e.g. '/c/en/cat' (Different than lookup API!)
SUPPORTED_ASSOCIATION_ARGS = ['filter', 'limit']

# Supported arguments for Search API
# :param {rel, start, end, node, source}: giving a ConceptNet URI for any of these
#       parameters will return edges whose corresponding fields start with the given path
# :type {rel, start, end, node, source}: uri
# :param node: returns edges whose rel, start, or end start with the given URI
# :type node: uri
# :param limit: change the number of results from the default of 50
# :type limit: integer
# :param filter: If 'core', only get edges from the ConceptNet 5 Core (not from ShareAlike resources),
#       if 'core-assetions', search for edges by default, and there can be many edges representing the same assertion.
# :type filter: Either 'core' or 'core-assertions'
SUPPORTED_SEARCH_ARGS = ['start', 'end', 'rel', 'node', 'sources', 'other', 'limit', 'filter']


# I filted out my instered Chinese commonsense.

intered_lang = 'zh'