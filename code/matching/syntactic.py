# coding=utf-8
"""
syntactic matching

"""
from utils.tree_edit_distance import distance
from utils.tree_edit_distance import postorder
from utils.tree_edit_distance import Node
from idf import idf

def print_tree_edit_distance(tree, idf_enabled=False, **kwargs):
    print "printing tree edit distance"
    for k, d, h, t in generate_edit_distance(tree, idf=idf_enabled):
        print k, "distance:", d

def tree_edit_distance(tree, idf_enabled=False, **kwargs):
    print "doing tree edit distance"
    classification = []
    for k, d, hypothesis, text in generate_edit_distance(tree, idf=idf_enabled):
        # a shorter distance corresponds to a high score
        normalized = 1-(d/float(hypothesis_to_none_ted(hypothesis)))
        classification.append((int(k), normalized))
        print normalized
    return classification


def generate_edit_distance(tree, idf=False):
    keys = tree.keys()
    keys = map(int, keys)
    keys.sort()
    for k in keys:
        k = str(k)
        hypothesis = tree[k]["hypothesis"]
        text = tree[k]["text"]
        print k
        if idf:
            d = distance(hypothesis, text, idf_cost)
        else:
            d = distance(hypothesis, text)
        yield k, d, hypothesis, text


def idf_cost(node1, node2):
    #TODO: get the idf value for the insertion value
    #delete
    if node1 is None: 
        return 0
    #insert
    if node2 is None: 
        if node1.name.startswith("E"):
            return 0
        if node1.word:
            return idf[node1.word]
        return 1
    if node1.label != node2.label: #substitution
        return 1
    else: # they are the same
        return 0

def hypothesis_to_none_ted(hypothesis):
    d = distance(hypothesis, Node("E", "join", ""))
    return d
