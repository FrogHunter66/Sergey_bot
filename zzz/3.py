def read_input():
    n = int(input())
    paths = [input() for _ in range(n)]
    return paths


def tree(paths):
    tree = {}
    for path in paths:
        directories = path.split('/')
        current_node = tree
        for directory in directories:
            if directory not in current_node:
                current_node[directory] = {}
            current_node = current_node[directory]
    return tree


def print_tree(tree, space=0):
    for directory in sorted(tree.keys()):
        print(' ' * space + directory)
        print_tree(tree[directory], space + 2)



paths = read_input()
tree = tree(paths)
print_tree(tree)
