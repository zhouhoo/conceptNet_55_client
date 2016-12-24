# import pynlpir # 中文分词，关键字
import os
import re
from collections import defaultdict

from hanziconv import HanziConv  # 简繁转换
from jieba import cut

from interface.api import LookUp, Search, Association
from utils.result import Result
from utils.translate import Translate


class Query:
    def __init__(self, debug=False):

        self.stop_word = ["的", "了", "在", "是", "我", "有", "和", "就",
                          "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
                          "会", "着", "没有", "看", "好", "自己", "这", "在于", "下",
                          '三', '四', '五', '六', '七', '八', '九', '十']
        self.conceptions = []
        self.related_conceptions = list(tuple())
        self.commonsense = set()
        self.debug = debug

    def parse_sentence(self, sentence=''):
        """
        :param sentence: type str, input sentence
        :param sentence: type bool, auto-get relation，havn't implement for now
        :return:
        """

        sentence = re.sub("[\s+\d+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）“”]+", "", sentence)
        # print("after cut:"+sentence)
        conceptions = cut(sentence)
        self.conceptions = [item for item in conceptions if item not in self.stop_word]
        if self.debug:
            print(self.conceptions)

    @staticmethod
    def base_lookup(conception, Type='c', lang='zh', limit=100, s_to_t=True):
        lookup = LookUp(lang=lang, Type=Type, limit=limit)
        if s_to_t:
            data = lookup.search_concept(HanziConv.toTraditional(conception))
        else:
            data = lookup.search_concept(conception)
        r = Result(data)

        if r.get_num_found() > 0:
            return [(edge.surfaceText, edge.start, edge.end, edge.rel)
                    for edge in r.parse_all_edges()]
        return None

    def concept_lookup(self):
        """

        :param concept:
        :return:
        """
        print('find only one conception,so get its commonsense at most 10')

        # 先中文查找
        local_commonsense = Query.base_lookup(HanziConv.toTraditional(self.conceptions))

        if not local_commonsense:
            # 如果没有找到，翻译成英文再次查找
            local_commonsense = Query.base_lookup(Translate.zh_to_en(self.conceptions))
        self.commonsense = set(local_commonsense)

    @staticmethod
    def base_search(conceptions, lang='zh'):

        res = list()
        for i in range(len(conceptions)):
            conception = '/c/' + lang + '/' + conceptions[i]
            s = Search(node=conception)  # can add more key-value
            data = s.search()
            r = Result(data)

            if r.get_num_found() > 0:
                tmp = [(edge.surfaceText, edge.start['term'].split('/')[3], edge.end['term'].split('/')[3],
                        edge.rel['label'])
                       for edge in r.parse_all_edges()]

                res.extend(tmp)

        return res

    def concept_search(self, to_traditional=True):

        # print('looking for  conceptions all related commonsense')
        if not self.conceptions:
            return
        if to_traditional:
            translated_conceptions = HanziConv.toTraditional(' '.join(self.conceptions))
            conceptions = translated_conceptions.split()
        else:
            conceptions = self.conceptions

        if self.debug:
            print("关键词：" + ''.join(conceptions))
        data = Query.base_search(conceptions)

        # if not data:
        #     translated_conceptions = Translate.zh_to_en(self.conceptions)
        #
        #     data = Query.base_search(translated_conceptions, lang='en')

        if data:
            self.commonsense = self.commonsense.union(set(data))

    @staticmethod
    def base_association(terms, lang='zh', limit=100):

        a = Association(lang=lang, limit=limit)
        raw_data = a.get_similar_concepts_by_term_list(terms)
        r = Result(raw_data)
        return r.parse_all_similarity()

    def conception_association(self):

        translated_conception = HanziConv.toTraditional(' '.join(self.conceptions))
        if self.debug:
            print(translated_conception)
        self.related_conceptions = Query.base_association(translated_conception.split())

    def tranlate_to_simple(self):

        for item in self.commonsense.copy():
            text = HanziConv.toSimplified(item[0]) if item[0] else 'No text'
            s = HanziConv.toSimplified(item[1])
            e = HanziConv.toSimplified(item[2])

            self.commonsense.remove(item)
            self.commonsense.add((text, s, e, item[3]))

    def commonsense_query(self, sentences):

        self.parse_sentence(sentences)

        self.concept_search(False)

        # self.conception_association()

        # self.tranlate_to_simple()
        # print(self.commonsense)
        return self.commonsense

    def stastics(self):
        len_conceptiton = len(self.conceptions)
        relation = defaultdict(int)
        pairs = set()
        text_info = set()
        f = open('../output/result.txt', 'w', encoding='utf-8')
        for edge in self.commonsense:
            relation[edge[3]] += 1
            pairs.add(edge[1] + '-' + edge[2])
            text_info.add(edge[0])
            f.writelines(str(edge) + '\n')

        import operator
        relation = sorted(relation.items(), key=operator.itemgetter(1))

        ff = open('../output/relation.txt', 'w', encoding='utf-8')
        ff.write(str(relation))
        # print(pairs)
        # print(text_info)

        print('原有概念数目：', len_conceptiton)
        if len_conceptiton:
            print("新引出概念对/ 原有的概念：", len(pairs) / len_conceptiton)
        print("引出的关系数目：", len(relation))
        # print("相似概念数目比例为：", len(self.related_conceptions)/len_conceptiton)

    def print_conceptions(self):
        print("常识描述文本---头结点概念----尾节点概念----关系")
        for item in self.commonsense:
            print(item)


if __name__ == "__main__":
    query = Query(debug=False)

    # sentences = ["找寻新的利润增长点成为摆在各行面前的一大课题。在资产荒的背景下，个人房贷成为各家银行争抢的“香饽饽”，但随着多地推出楼市调控政策，按揭贷款或将从11月开始有所回落。",
    #             "精准医疗的目的是进行个体化定制治疗。因为每个人都存在着个体化差异，就算患上同一种疾病，在病理表现上也是不同的，可以表现为基因水平和蛋白水平上的差异",
    #              "全国人大常委会表决通过网络安全法，特别增加了惩治网络诈骗的有关规定，对个人信息保护做出规定，要求网络运营者应当采取技术措施和其他必要措施，确保其收集的个人信息安全，防止信息泄露、毁损、丢失"]

    files = ["../data/" + f for f in os.listdir("../data/")]
    for file in files:
        print(file)
        with open(file, encoding='utf-8') as f:
            data = f.readlines()

            data_filtered = [s.replace(' ', '') for s in data if not s.isspace() and '---' not in s]

            sentences = ''.join(data_filtered).split("。")

            for sentence in sentences:
                # print("句子是"+sentence)
                query.commonsense_query(sentence)

        query.stastics()
