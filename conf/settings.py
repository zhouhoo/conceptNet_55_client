# These URLs basically points to MIT's conceptnet5 setup for Web API
# BASE_LOOKUP_URL = 'http://api.conceptnet.io'
# BASE_SEARCH_URL = 'http://api.conceptnet.io/query'
# BASE_ASSOCIATION_URL = 'http://api.conceptnet.io/related'

# if build locall ,use those
BASE_LOOKUP_URL = 'http://127.0.0.1:8084'
BASE_SEARCH_URL = 'http://127.0.0.1:8084/query'
BASE_ASSOCIATION_URL = 'http://127.0.0.1:8084/related'

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

# Baidu translate service settings
base_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
appid = 'your appid'
secretKey = 'your secretKey'

LCODE_ALIASES = {
    # Pretend that various Chinese languages and variants are equivalent. This
    # is linguistically problematic, but it's also very helpful for aligning
    # them on terms where they actually are the same.
    #
    # This would mostly be a problem if ConceptNet was being used to *generate*
    # Chinese natural language text.
    'cmn': 'zh',
    'yue': 'zh',
    'zh_tw': 'zh',
    'zh_cn': 'zh',
    'zh-tw': 'zh',
    'zh-cn': 'zh',

    'nds-de': 'nds',
    'nds-nl': 'nds',

    # An easier case: consider Bahasa Indonesia and Bahasa Malay to be the
    # same language, with code 'ms', because they're already 90% the same.
    # Many sources use 'ms' to represent the entire macrolanguage, with
    # 'zsm' to refer to Bahasa Malay in particular.
    'zsm': 'ms',
    'id': 'ms',

    # We had to make a decision here on Norwegian. Norwegian Bokmål ('nb') and
    # Nynorsk ('nn') have somewhat different vocabularies but are mutually
    # intelligible. Informal variants of Norwegian, especially when spoken,
    # don't really distinguish them. Some Wiktionary entries don't distinguish
    # them either. And the CLDR data puts them both in the same macrolanguage
    # of Norwegian ('no').
    #
    # The catch is, Bokmål and Danish are *more* mutually intelligible than
    # Bokmål and Nynorsk, so maybe they should be the same language too. But
    # Nynorsk and Danish are less mutually intelligible.
    #
    # There is no language code that includes both Danish and Nynorsk, so
    # it would probably be inappropriate to group them all together. We will
    # take the easy route of making the language boundaries correspond to the
    # national boundaries, and say that 'nn' and 'nb' are both kinds of 'no'.
    #
    # More information: http://languagelog.ldc.upenn.edu/nll/?p=9516
    'nn': 'no',
    'nb': 'no',

    # Our sources have entries in Croatian, entries in Serbian, and entries
    # in Serbo-Croatian. Some of the Serbian and Serbo-Croatian entries
    # are written in Cyrillic letters, while all Croatian entries are written
    # in Latin letters. Bosnian and Montenegrin are in there somewhere,
    # too.
    #
    # Applying the same principle as Chinese, we will unify the language codes
    # into the macrolanguage 'sh' without unifying the scripts.
    'bs': 'sh',
    'hr': 'sh',
    'sr': 'sh',
    'hbs': 'sh',
    'sr-latn': 'sh',
    'sr-cyrl': 'sh',

    # More language codes that we would rather group into a broader language:
    'arb': 'ar',  # Modern Standard Arabic -> Arabic
    'arz': 'ar',  # Egyptian Arabic -> Arabic
    'ary': 'ar',  # Moroccan Arabic -> Arabic
    'ckb': 'ku',  # Central Kurdish -> Kurdish
    'mvf': 'mn',  # Peripheral Mongolian -> Mongolian
    'tl': 'fil',  # Tagalog -> Filipino
    'vro': 'et',  # Võro -> Estonian
    'sgs': 'lt',  # Samogitian -> Lithuanian
    'ciw': 'oj',  # Chippewa -> Ojibwe
    'xal': 'xwo',  # Kalmyk -> Oirat
    'ffm': 'ff',  # Maasina Fulfulde -> Fula
}
