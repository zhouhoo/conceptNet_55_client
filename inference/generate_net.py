import random

from ordered_set import OrderedSet

from app.ResultParse import ResultParse
from interface.api import LookUp

"""
##give a start node, at limited step to construct a connected nets with conceptions and relations.
"""


class netGenerator:
    def __init__(self, lang='zh', seed_concept='银行', step_limit=2):

        self.start_node = seed_concept
        self.edges = list()
        self.conceptions = OrderedSet([self.start_node])
        self.limit = step_limit
        self.has_looked = set()
        self.finder = LookUp(lang=lang)

    def generate_concept_relation(self, conception):

        data = self.finder.search_concept(conception)
        r = ResultParse(data)

        edges = r.parse_all_edges()
        if edges:
            for edge in edges:
                head = edge.start.split('/')[3]
                tail = edge.end.split('/')[3]
                self.conceptions.add(head)
                self.conceptions.add(tail)
                assertion = (head, tail, edge.rel)
                self.edges.append(assertion)

    def generate_next_start(self):

        fresh_conceptions = [c for c in self.conceptions if c not in self.has_looked]

        next_start = None
        if fresh_conceptions:
            index = random.randint(0, len(fresh_conceptions))
            next_start = fresh_conceptions[index]

        return next_start

    def run_generate(self):

        self.has_looked.add(self.start_node)
        self.generate_concept_relation(self.start_node)

        if len(self.conceptions) == 1:
            print("bad start point, can not walk foward!")
            exit(0)

        for step in range(self.limit):

            if len(self.conceptions) == len(self.has_looked):
                print("can not walk any more before step limit achieved!")
                break

            candidate = self.generate_next_start()
            self.has_looked.add(candidate)
            self.generate_concept_relation(candidate)

        assertions = list()
        for edge in self.edges:
            assertions.append((self.conceptions.index(edge[0]), self.conceptions.index(edge[1]), edge[2]))

        print(len(assertions))
        net = {'nodes': self.conceptions, 'edges': assertions}

        return net


if __name__ == '__main__':
    g = netGenerator()

    g.run_generate()
