import hashlib
import random
import urllib

from conf.settings import appid, secretKey, base_url
from tools.https import make_http_request


# I use Baidu translate service , you can set up your appid and secretKey in conf/setting.py


class Translate:
    def __init__(self, from_lang='zh', to_lang='en'):
        self.salt = str(random.randint(32768, 65536))

        self.query_url = base_url + \
                         '?appid=' + appid + \
                         '&from=' + from_lang + \
                         '&to=' + to_lang + \
                         '&salt=' + self.salt

    def zh_to_en(self, query_list):
        print(query_list)
        query_str = '\n'.join(query_list)
        sign = hashlib.md5((appid + query_str + self.salt + secretKey).encode('utf-8')).hexdigest()
        post_url = self.query_url + '&sign=' + sign + '&q=' + urllib.parse.quote(query_str)

        words_json = make_http_request(post_url)

        return [item['dst'] for item in words_json['trans_result']]


if __name__ == '__main__':
    query_words = ['汉子', '妹子']
    t = Translate()
    res = t.zh_to_en(query_words)

    print(res)
