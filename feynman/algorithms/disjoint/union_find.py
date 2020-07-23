from collections import defaultdict

from feynman.algorithms.tree.print_tree import print_tree

def get_parent(dic, x):
    if x not in dic:
        dic[x] = x

    if x == dic[x]:
        return x
    else:
        dic[x] = get_parent(dic, dic[x])
        return dic[x]


def union_parent(dic, parent, child):
    _parent = get_parent(dic, parent)
    _child = get_parent(dic, child)
    if _parent != _child:
        dic[_child] = _parent

if __name__ == '__main__':
    dic = {}
    data = [(100, 30),
            (30, 400),
            (30, 500),
            (0, 100),
            (0, 20),
            (0, 10),
            (60000, 600),
            (500, 495),
            (60000, 70),
            (60000, 80),
            (500, 496),
            (500, 497)]
    for parent, child in data:
        union_parent(dic, parent, child)

    disjoint = defaultdict(list)
    for child in dic.keys():
        if get_parent(dic, child) != child:
            disjoint[get_parent(dic, child)].append(child)

    for k, v in disjoint.items():
        print('{}:{}'.format(k, v))
