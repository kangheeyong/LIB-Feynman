
def print_tree(start, tree, func=lambda x: x, indent_width=2):

    def _print_tree(start, parent, tree, grandpa=None, indent=""):
        if parent != start:
            if grandpa is None:  # Ask grandpa kids!
                print(func(parent), end="")
            else:
                print(func(parent))
        if parent not in tree:
            return
        for child in tree[parent][:-1]:
            print(indent + "├" + "─" * indent_width, end="")
            _print_tree(start, child, tree, parent, indent + "│" + " " * indent_width)
        child = tree[parent][-1]
        print(indent + "└" + "─" * indent_width, end="")
        _print_tree(start, child, tree, parent, indent + " " * (indent_width+1))  # 4 -> 5

    parent = start
    print(parent)
    _print_tree(start, parent, tree)


if __name__ == '__main__':

    dct = {
        -1: [0, 60000],
        0: [100, 20, 10],
        100: [30],
        30: [400, 500],
        60000: [70, 80, 600],
        500: [495, 496, 497]
    }

    print_tree(-1, dct)
