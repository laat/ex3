# coding=utf-8
"""
syntactic matching

"""
from utils.tree_edit_distance import distance
from utils.tree_edit_distance import postorder

def print_tree_edit_distance(tree):
    keys = tree.keys()
    keys = map(int, keys)
    keys.sort()
    for k in keys:
        k = str(k)
        d = distance(tree[k]["hypothesis"], tree[k]["text"])
        print k, "distance:", d

