
def bfs(g, start):
    qu = list()
    done = set()
    qu.append(start)
    done.add(start)
    while qu:
        p = qu.pop(0)
        yield p, g.get(p, [])
        for x in g.get(p, []):
            if x not in done:
                qu.append(x)
                done.add(x)

if __name__ == '__main__':

    dct = {
        -1: [0, 60000],
        0: [100, 20, 10],
        100: [30],
        30: [400, 500],
        60000: [70, 80, 600],
        500: [495, 496, 497]
    }
    for parent, children in bfs(dct, -1):
        print('{}:{}'.format(parent, children))
