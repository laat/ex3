#coding=utf-8
from utils.tree_edit_distance import Node
from xml.etree.ElementTree import iterparse
from collections import defaultdict


def generate_syntax_tree(file_name):
    """
    Parses the xmlfile
    """
    pairs = {}
    for event, elem in iterparse(file_name):
        if elem.tag == "pair":
            pair = {}
            for child in elem.getchildren():
                tag = child.tag
                sentences = []
                for sentence in child.getchildren():
                    serial = sentence.get('serial')
                    roots, nodes_by_id, nodes_by_parent = sainitize_sentence(sentence)
                    for root in roots:
                        sentences.append(create_node_tree(root, nodes_by_id, nodes_by_parent, serial))

                sentences = join_roots(sentences)
                pair[tag] = sentences
            pairs[elem.get('id')] = pair
    return pairs

def join_roots(roots):
    """
    joines a forest of nodes under one root node
    """

    roots.sort()  # order still matters
    if len(roots) == 1:
        return roots[0]
    elif len(roots) > 1:
        n_root = Node("E", "join", "")
        n_root.extend(roots)
        return n_root
    else:
        print "WTF", roots

def sainitize_sentence(sentence):
    """
    Parses the sentence madness into something usable
    sentence is a ElementTree object
    """
    roots = []
    nodes_by_id = {}  # {id : (id, lemma)}
    nodes_by_parent = defaultdict(list)  # {parent_id: (id, lemma)}

    for node in sentence.iterfind('node'):
        node_id = node.get('id')
        node_lemma = node.find('lemma')
        node_word = node.find('word')

        if node_lemma != None:
            node_lemma = node_lemma.text.strip().rstrip().lower()

        if node_word != None:
            node_word = node_word.text.strip().rstrip().lower()

        node_relation = node.find('relation')

        if node_lemma != None:
            nodes_by_id[node_id] = (node_id, node_lemma, node_word)

        if node_relation != None and node_lemma != None:
            parent = node_relation.get('parent')
            nodes_by_parent[parent].append( (node_id, node_lemma, node_word))

        if node_relation == None:
                roots.append((node_id, "", None))

    #print roots
    return roots, nodes_by_id, nodes_by_parent


def create_node_tree(start,nodes_by_id, nodes_by_parent, serial):
    """
    creates a node tree
    nodes_by_id:        is a dict with (node_id, node_lemma) as values with the
                        node id as the key
    nodes_by_parent:    is a dict with (node_id, node_lemma) as walyes with the
                        parent node id as the key
    """
    #BFS
    root = Node(start[0], start[1], serial, word=start[2])
    stack = [root]  # labels
    while len(stack):
        node = stack.pop(0)
        children = get_children(node, nodes_by_id, nodes_by_parent)
        children_nodes = [Node(child[0], child[1], serial, word=child[2]) for child in children]
        if children:
            node.extend(children_nodes)
            stack.extend(children_nodes)
    return root



def get_children(node, nodes_by_id, nodes_by_parent):
    """ 
    returns a list of children for the given node 
    """
    children = []
    for child in nodes_by_parent[node.name]:
        children.append(child)

    #XML is broken anyways, and does not contain information of the order if
    #children
    children.sort()
    return children
