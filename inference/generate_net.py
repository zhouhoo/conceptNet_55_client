import csv
import random

import networkx as nx
from ordered_set import OrderedSet

from app.ResultParse import ResultParse
from interface.api import LookUp

try:
    import matplotlib.pyplot as plt
    import matplotlib
except:
    raise

matplotlib.rc('font', family='DejaVu Sans')
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
                assertion = (head, tail, edge.weight, edge.rel)
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

            if not candidate:
                continue

            self.has_looked.add(candidate)
            self.generate_concept_relation(candidate)

    def get_and_save_to_csv(self, filepath='../output/net.csv'):

        with open(filepath, 'w', encoding='utf-8') as output:
            wr = csv.writer(output, lineterminator='\n')
            wr.writerows(self.edges)

        net = {'nodes': self.conceptions, 'edges': self.edges}

        return net

    def get_and_save_to_gexf(self, filepath='../output/net.gexf'):

        net = nx.DiGraph()

        for ind, item in enumerate(self.conceptions):
            net.add_node(ind, {'attvalues': ind}, label=item)
            x = random.uniform(0, 600)
            y = random.uniform(0, 600)
            r = random.randint(0, 256)
            g = random.randint(0, 256)
            b = random.randint(0, 256)
            net.node[ind]['viz'] = {'color': {'r': r, 'g': g, 'b': b, 'a': 0},
                                    'size': 50,
                                    'position': {'x': x, 'y': y, 'z': 0}}

        assertions = list()
        for edge in self.edges:
            u = self.conceptions.index(edge[0])
            v = self.conceptions.index(edge[1])
            assertions.append((u, v, edge[2], edge[3]))
            net.add_edge(u, v, label=edge[3], weight=edge[2])

        nx.write_gexf(net, filepath, encoding='utf-8', version="1.2draft")

        net_data = {'nodes': self.conceptions, 'edges': assertions}

        return net_data

    def plot_and_save_net(self, picpath='../output/net.png'):

        net = nx.DiGraph()

        edge_label = dict()
        for edge in self.edges:
            net.add_edge(edge[0], edge[1], weight=1)
            edge_label[(edge[0], edge[1])] = edge[2]
            if len(edge_label) > 8:
                break
                # edge_label.update({(edge[0], edge[1]) : edge[2]})

        pos = nx.spring_layout(net, k=20)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(net, pos, node_size=6000, node_color="green")

        # edges
        nx.draw_networkx_edges(net, pos,
                               width=1.5, alpha=0.5, arrows=True, edge_color='black')
        # labels
        nx.draw_networkx_labels(net, pos, font_size=20, font_family='sans-serif')

        nx.draw_networkx_edge_labels(net, pos, edge_labels=edge_label, label_pos=0.5)

        plt.axis('off')
        plt.savefig(picpath)  # save as png
        plt.show()  # display

if __name__ == '__main__':
    gg = netGenerator()
    gg.run_generate()
    gg.get_and_save_to_csv()
    # G=nx.DiGraph()
    #
    # a="我"
    # b="是"
    # c="你"
    # d="好"
    # G.add_edge(a,b,weight=0.5)
    # G.add_edge(b,c,weight=0.5)
    # G.add_edge(c,d,weight=0.5)
    # G.add_edge(a,d,weight=0.5)
    # G.add_edge(a,c,weight=0.5)
    # G.add_edge(b,d,weight=0.5)
    #
    # pos=nx.spring_layout(G) # positions for all nodes
    #
    # # nodes
    # nx.draw_networkx_nodes(G,pos,node_size=7000, node_color="white")
    #
    # # edges
    # nx.draw_networkx_edges(G,pos,
    #                        width=6,alpha=0.5,edge_color='black')
    #
    #
    # # labels
    # nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
    #
    # nx.draw_networkx_edge_labels(G,pos,
    #                              {
    #                                  (a,b):"x", (b,c):"y", (c,d):"w", (a,d):"z", (a,c):"v", (b,d):"r"
    #                              }
    #                              )
    #
    # plt.axis('off')
    # plt.savefig("weighted_graph.png") # save as png
    # plt.show() # display
