from collections import defaultdict, namedtuple

from Feynman.algorithms.disjoint.union_find import get_parent, union_parent
from Feynman.algorithms.graph.bfs import bfs


class Google_drive_data_base():
    def __init__(self, data, root='0AGVYmV18tFTYUk9PVA'):
        self._data = data
        self._edge_list = self._make_edge_list()

        self.root = root
        self.all_dic = defaultdict(list)
        self.adj_dic = self._make_adj_dic()
        self.data_dic = self._make_dic()
        self.view_dic = defaultdict(list)
        self.remove_set = set()

    def _make_edge_list(self):
        EdgeList = namedtuple('listuple', 'child parent')
        edge_list = list()
        for d in self._data:
            child = d['id']
            for parent in d['parents']:
                edge_list.append(EdgeList(child=child, parent=parent))
        return edge_list

    def _make_adj_dic(self):
        adj_dic = defaultdict(list)
        for d in self._data:
            child = d['id']
            for parent in d['parents']:
                adj_dic[parent].append(child)
        return adj_dic

    def _make_dic(self):
        dic = defaultdict()
        for i, d in enumerate(self._data):
            child = d['id']
            for parent in d['parents']:
                dic[child] = d
        return dic

    def pruning_overlap_file(self, max_size=1):
        for parent, children in bfs(self.adj_dic, self.root):
            qu = defaultdict(list)
            if not children:
                continue
            for child in children:
                qu[self.data_dic[child]['name']].append(child)
            for filename in qu.keys():
                qu[filename].sort(key=lambda x: self.data_dic[x]['createdTime'], reverse=True)
            for filename in qu.keys():
                self.remove_set.update(qu[filename][max_size:])
                self.view_dic[parent] += qu[filename][:max_size]

    def pruning_zombie_file(self):
        dic = defaultdict(str)
        for child, parent in self._edge_list:
            union_parent(dic, parent, child)
        for child, _ in self._edge_list:
            if get_parent(dic, child) != child:
                self.all_dic[get_parent(dic, child)].append(child)
        for root in self.all_dic.keys():
            if root != self.root:
                self.remove_set.update(self.all_dic[root])
