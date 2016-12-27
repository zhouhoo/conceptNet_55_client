import re

from jieba import cut

chiese_stop_word = ["的", "了", "在", "是", "我", "有", "和", "就",
                    "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
                    "会", "着", "没有", "看", "好", "自己", "这", "在于", "下",
                    '三', '四', '五', '六', '七', '八', '九', '十']

english_STOPWORDS = [
    'the', 'a', 'an'
]

DROP_FIRST = ['to']

filter_patten = "[\s+\d+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）“”]+"


def parse_sentence(sentence=''):
    """
    :param sentence: type str, input sentence
    :param sentence: type bool, auto-get relation，havn't implement for now
    :return:
    """

    sentence = re.sub(filter_patten, "", sentence)

    conceptions = chinese_filter(cut(sentence))

    return conceptions


def chinese_filter(tokens):
    non_stopwords = [token for token in tokens if token not in chiese_stop_word]

    return non_stopwords


def english_filter(tokens):
    """
    Given a list of tokens, remove a small list of English stopwords.
    """
    non_stopwords = [token for token in tokens if token not in english_STOPWORDS]
    while non_stopwords and non_stopwords[0] in DROP_FIRST:
        non_stopwords = non_stopwords[1:]
    if non_stopwords:
        return non_stopwords
    else:
        return tokens
