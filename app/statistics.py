import operator
from collections import defaultdict


class analysis:
    def __init__(self, file_path='../output/'):

        self.file_path = file_path
        self.relation = defaultdict(int)
        self.pairs = set()
        self.text_info = set()

    def write_commonsense(self, commonsense):

        f = open(self.file_path + 'result.txt', 'w', encoding='utf-8')
        for edge in commonsense:
            self.relation[edge[3]] += 1
            self.pairs.add(edge[1] + '-' + edge[2])
            self.text_info.add(edge[0])
            f.writelines(str(edge) + '\n')

    def write_all_relations(self):

        relation = sorted(self.relation.items(), key=operator.itemgetter(1))

        ff = open(self.file_path + 'relation.txt', 'w', encoding='utf-8')
        ff.write(str(relation))

    def print_comparation(self, len_conceptiton):

        print('原有概念数目：', len_conceptiton)
        if len_conceptiton:
            print("新引出概念对/ 原有的概念：", len(self.pairs) / len_conceptiton)
        print("引出的关系数目：", len(self.relation))

    def print_conceptions(self, commonsense):
        print("常识描述文本---头结点概念----尾节点概念----关系")
        for item in commonsense:
            print(item)
