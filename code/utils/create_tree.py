#coding=utf-8
from utils.tree_edit_distance import Node
from xml.etree.ElementTree import iterparse
from collections import defaultdict


def generate_syntax_tree(file_name):
    pairs = {}
    for event, elem in iterparse(file_name):
        if elem.tag == "pair":
            pair = {}
            for child in elem.getchildren():
                tag = child.tag
                sentences = []
                for sentence in child.getchildren():
                    roots, nodes_by_id, nodes_by_parent = sainitize_sentence(sentence)
                    forest = []
                    for root in roots:
                        forest.append(create_node_tree(root, nodes_by_id, nodes_by_parent))
                    sentences.append(forest)
                pair[tag] = sentences
            pairs[elem.get('id')] = pair
    return pairs

def sainitize_sentence(sentence):
    roots = []
    nodes_by_id = {}  # {id : (id, lemma)}
    nodes_by_parent = defaultdict(list)  # {parent_id: (id, lemma)}

    for node in sentence.iterfind('node'):
        node_id = node.get('id')
        node_lemma = node.find('lemma')
        if node_lemma != None:
            node_lemma = node_lemma.text.strip().rstrip()
        node_relation = node.find('relation')
        if node_lemma != None:
            nodes_by_id[node_id] = node_id, node_lemma
            if node_lemma == "fin":
                roots.append((node_id, node_lemma)) # the roots in the forest
        if node_relation != None and node_lemma != None:
            parent = node_relation.get('parent')
            nodes_by_parent[parent].append( (node_id, node_lemma))

    #print roots
    return roots, nodes_by_id, nodes_by_parent


def create_node_tree(start,nodes_by_id, nodes_by_parent):
    #BFS
    root = Node(start[0], start[1])
    stack = [root]  # labels
    while len(stack):
        node = stack.pop(0)
        children = get_children(node, nodes_by_id, nodes_by_parent)
        children_nodes = [Node(child[0], child[1]) for child in children]
        if children:
            node.extend(children_nodes)
            stack.extend(children_nodes)
    return root



def get_children(node, nodes_by_id, nodes_by_parent):
    children = []
    for child in nodes_by_parent[node.name]:
        children.append(child)

    #XML is broken anyways, and does not contain information of the order if
    #children
    #children.sort()
    return children
