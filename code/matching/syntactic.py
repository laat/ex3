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
        normalized = 0
        if idf:
            normalized = 1-(d/(float(hypothesis_to_none_ted(hypothesis,
                                     idf_enabled=idf_enabled))))
        else:
            normalized = 1-(d/float(hypothesis_to_none_ted(hypothesis)))

        classification.append((int(k), normalized))
        if normalized > 1: 
            print"key:", k, "distance:", d, "hyp_len", hypothesis_to_none_ted(hypothesis)
    return classification


def generate_edit_distance(tree, idf=False):
    keys = tree.keys()
    keys = map(int, keys)
    keys.sort()
    for k in keys:
        k = str(k)
        hypothesis = tree[k]["hypothesis"]
        text = tree[k]["text"]
        if idf:
            d = distance(text, hypothesis, costs=idf_cost)
        else:
            d = distance(text,hypothesis)
        yield k, d, hypothesis, text


def idf_cost(node1, node2):
    #TODO: get the idf value for the insertion value
    #insert
    if node1 is None: 
        if node2.word:
            return idf[node2.word]
        else:
            return 0
    #delete
    if node2 is None: 
        return 0

    #substitution
    if node1.label != node2.label:
        return 1
    else: # they are the same
        return 0

def hypothesis_to_none_ted(hypothesis, idf_enabled=False):
    if idf_enabled:
        d = distance(Node("E", "join", ""), hypothesis, costs=idf_cost)
    else:
        d = distance(Node("E", "join", ""), hypothesis)
    return d
