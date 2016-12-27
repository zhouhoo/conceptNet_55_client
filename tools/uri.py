import unicodedata

import regex

from conf.settings import LCODE_ALIASES
from tools.parse_and_filter import chinese_filter, english_filter

SPACELESS_SCRIPTS = [
    'Hiragana',
    'Thai',  # Thai script
    'Khmr',  # Khmer script
    'Laoo',  # Lao script
    'Mymr',  # Burmese script
    'Tale',  # Tai Le script
    'Talu',  # Tai Lü script
    'Lana',  # Lanna script
]


def make_spaceless_expr():
    pieces = [r'\p{IsIdeo}'] + [r'\p{Script=%s}' % script_code for script_code in SPACELESS_SCRIPTS]
    return ''.join(pieces)


TOKEN_RE_WITH_PUNCTUATION = regex.compile(r"""
    [<SPACELESS>]+ |
    [\p{punct}]+ |
    \S(?:\B\S|\p{M})*
""".replace('<SPACELESS>', make_spaceless_expr()), regex.V1 | regex.WORD | regex.VERBOSE)

TOKEN_RE = regex.compile(r"""
    # Case 1: a special case for non-spaced languages
    # -----------------------------------------------

    # Some scripts are written without spaces, and the Unicode algorithm
    # seems to overreact and insert word breaks between all their letters.
    # When we see sequences of characters in these scripts, we make sure not
    # to break them up. Such scripts include Han ideographs (\p{IsIdeo}),
    # hiragana (\p{Script=Hiragana}), and many Southeast Asian scripts such
    # as Thai and Khmer.
    #
    # Without this case, the standard rule (case 2) would make each character
    # a separate token. This would be the correct behavior for word-wrapping,
    # but a messy failure mode for NLP tokenization.
    #
    # If you have Chinese or Japanese text, it's certainly better to use a
    # tokenizer that's designed for it. Elsewhere in this file, we have
    # specific tokenizers that can handle Chinese and Japanese. With this
    # rule, though, at least this general tokenizer will fail less badly
    # on those languages.
    #
    # This rule is listed first so that it takes precedence. The placeholder
    # <SPACELESS> will be replaced by the complex range expression made by
    # _make_spaceless_expr().

    [<SPACELESS>]+ |

    # Case 2: standard Unicode segmentation
    # -------------------------------------

    # The start of the token must be 'word-like', not punctuation or whitespace
    # or various other things. However, we allow characters of category So
    # (Symbol - Other) because many of these are emoji, which can convey
    # meaning.

    [\w\p{So}]

    # The rest of the token matches characters that are not any sort of space
    # (\S) and do not cause word breaks according to the Unicode word
    # segmentation heuristic (\B), or are categorized as Marks (\p{M}).

    (?:\B\S|\p{M})*
""".replace('<SPACELESS>', make_spaceless_expr()), regex.V1 | regex.WORD | regex.VERBOSE)


def simple_tokenize(text, include_punctuation=False):
    """
    Tokenize the given text using a straightforward, Unicode-aware token
    expression.

    The expression mostly implements the rules of Unicode Annex #29 that
    are contained in the `regex` module's word boundary matching, including
    the refinement that splits words between apostrophes and vowels in order
    to separate tokens such as the French article «l'». Our customizations
    to the expression are:

    - It leaves sequences of Chinese or Japanese characters (specifically, Han
      ideograms and hiragana) relatively untokenized, instead of splitting each
      character into its own token.

    - If `include_punctuation` is False (the default), it outputs only the
      tokens that start with a word-like character, or miscellaneous symbols
      such as emoji. If `include_punctuation` is True, it outputs all non-space
      tokens.

    - It breaks on all spaces, even the "non-breaking" ones.

    - It aims to keep marks together with words, so that they aren't erroneously
      split off as punctuation in languages such as Hindi.

    - It keeps Southeast Asian scripts, such as Thai, glued together. This yields
      tokens that are much too long, but the alternative is that every character
      would end up in its own token, which is worse.
    """
    text = unicodedata.normalize('NFC', text)
    token_expr = TOKEN_RE_WITH_PUNCTUATION if include_punctuation else TOKEN_RE
    return [token.strip("'").casefold() for token in token_expr.findall(text)]


def standardize_text(text, token_filter=None):
    """
    Get a string made from the tokens in the text, joined by
    underscores. The tokens may have a language-specific `token_filter`
    applied to them. See `standardize_as_list()`.

        >>> standardize_text(' cat')
        'cat'

        >>> standardize_text('a big dog', token_filter=english_filter)
        'big_dog'

        >>> standardize_text('Italian supercat')
        'italian_supercat'

        >>> standardize_text('a big dog')
        'a_big_dog'

        >>> standardize_text('a big dog', token_filter=english_filter)
        'big_dog'

        >>> standardize_text('to go', token_filter=english_filter)
        'go'

        >>> standardize_text('Test?!')
        'test'

        >>> standardize_text('TEST.')
        'test'

        >>> standardize_text('test/test')
        'test_test'

        >>> standardize_text('   u\N{COMBINING DIAERESIS}ber\\n')
        'über'

        >>> standardize_text('embedded' + chr(9) + 'tab')
        'embedded_tab'

        >>> standardize_text('_')
        ''

        >>> standardize_text(',')
        ''
    """
    tokens = simple_tokenize(text.replace('_', ' '))
    if token_filter is not None:
        tokens = token_filter(tokens)
    return '_'.join(tokens)


def join_uri(*pieces):
    """
    `join_uri` builds a URI from constituent pieces that should be joined
    with slashes (/).

    Leading and trailing on the pieces are acceptable, but will be ignored.
    The resulting URI will always begin with a slash and have its pieces
    separated by a single slash.

    The pieces do not have `standardize_text` applied to them; to make sure your
    URIs are in normal form, run `standardize_text` on each piece that represents
    arbitrary text.

    >>> join_uri('/c', 'en', 'cat')
    '/c/en/cat'

    >>> join_uri('c', 'en', ' spaces ')
    '/c/en/ spaces '

    >>> join_uri('/r/', 'AtLocation/')
    '/r/AtLocation'

    >>> join_uri('/test')
    '/test'

    >>> join_uri('test')
    '/test'

    >>> join_uri('/test', '/more/')
    '/test/more'
    """
    joined = '/' + ('/'.join([piece.strip('/') for piece in pieces]))
    return joined


def concept_uri(lang, text, *more):
    """
    `concept_uri` builds a representation of a concept, which is a word or
    phrase of a particular language, which can participate in relations with
    other concepts, and may be linked to concepts in other languages.

    Every concept has an ISO language code and a text. It may also have a part
    of speech (pos), which is typically a single letter. If it does, it may
    have a disambiguation, a string that distinguishes it from other concepts
    with the same text.

    This function should be called as follows, where arguments after `text`
    are optional:

        concept_uri(lang, text, pos, disambiguation...)

    `text` and `disambiguation` should be strings that have already been run
    through `standardize_text`.

    This is a low-level interface. See `standardized_concept_uri` in nodes.py for
    a more generally applicable function that also deals with special
    per-language handling.

    >>> concept_uri('en', 'cat')
    '/c/en/cat'
    >>> concept_uri('en', 'cat', 'n')
    '/c/en/cat/n'
    >>> concept_uri('en', 'cat', 'n', 'feline')
    '/c/en/cat/n/feline'
    >>> concept_uri('en', 'this is wrong')
    Traceback (most recent call last):
        ...
    AssertionError: 'this is wrong' is not in normalized form
    """
    assert ' ' not in text, "%r is not in normalized form" % text
    if len(more) > 0:
        if len(more[0]) != 1:
            # We misparsed a part of speech; everything after the text is
            # probably junk
            more = []
        for dis1 in more[1:]:
            assert ' ' not in dis1, \
                "%r is not in normalized form" % dis1

    return join_uri('/c', lang, text, *more)


def standardized_concept_uri(lang, text, *more):
    """
    Make the appropriate URI for a concept in a particular language, including
    stemming the text if necessary, normalizing it, and joining it into a
    concept URI.

    Items in 'more' will not be stemmed, but will go through the other
    normalization steps.

    >>> standardized_concept_uri('en', 'this is a test')
    '/c/en/this_is_test'
    >>> standardized_concept_uri('en', 'this is a test', 'n', 'example phrase')
    '/c/en/this_is_test/n/example_phrase'
    """
    if lang == 'en':
        token_filter = english_filter
    elif lang == 'zh':
        token_filter = chinese_filter
    else:
        token_filter = None

    lang = lang.lower()
    if lang in LCODE_ALIASES:
        lang = LCODE_ALIASES[lang]
    norm_text = standardize_text(text, token_filter)
    more_text = [standardize_text(item, token_filter) for item in more
                 if item is not None]
    return concept_uri(lang, norm_text, *more_text)
