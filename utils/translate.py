import hashlib
import random
import urllib

from utils.https import make_http_request

appid = '20160923000029198'
secretKey = 'uJ5PMHV18mR7c_4CQEoi'


class Translate:
    appid = '20160923000029198'
    secretKey = 'uJ5PMHV18mR7c_4CQEoi'
    salt = str(random.randint(32768, 65536))
    base_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'zh'
    toLang = 'en'
    query_url = base_url + \
                '?appid=' + appid + \
                '&from=' + fromLang + \
                '&to=' + toLang + \
                '&salt=' + salt

    @classmethod
    def zh_to_en(cls, query_list):
        print(query_list)
        query_str = '\n'.join(query_list)
        sign = hashlib.md5((appid + query_str + cls.salt + secretKey).encode('utf-8')).hexdigest()
        post_url = cls.query_url + '&sign=' + sign + '&q=' + urllib.parse.quote(query_str)

        words_json = make_http_request(post_url)

        return [item['dst'] for item in words_json['trans_result']]


if __name__ == '__main__':
    query_words = ['汉子', '妹子']
    res = Translate.zh_to_en(query_words)

    print(res)
