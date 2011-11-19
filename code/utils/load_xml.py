# coding=utf-8
"""
This file handels parsing of the trainingdata in the XML
"""

from xml.etree import ElementTree as ET
import os


def get_pairs(input_file):
    tree = get_tree(input_file)
    # generate a pairs list
    pairs = []
    for pair in tree.getroot():
        id = pair.attrib['id']
        text = get_sentences(pair.find('text'))
        hypothesis = get_sentences(pair.find('hypothesis'))
        task = pair.attrib['task']
        entailment = pair.attrib['entailment']

        pairs.append(Pair(id, text, hypothesis, entailment, task))
    return pairs

def get_sentences(tree):
    sentences = []
    for s in tree:
        terms = get_terms(s)
        serial = s.attrib['serial']
        
        sentence = Sentence(serial, terms)
        sentences.append(sentence)
    return sentences

def get_terms(sentence):
    terms = []
    for t in sentence:
        id = t.attrib["id"]
        word = _find_lower(t, "word")
        pos = _find_lower(t, "pos-tag")
        lemma = _find_lower(t, "lemma")
        try:
            relation = (_find_lower(t, "relation"),
                    t.find("relation").attrib["parent"])
        except AttributeError:
            relation = None

        terms.append(Term(id, word, pos, relation, lemma))
    return terms

def _find_lower(t, term):
    try:
        return t.find(term).text.strip().lower()
    except AttributeError:
        return  # det er normalt at noen attributter ikke finnes

def get_tree(input_file):
    try:
       tree = ET.parse(input_file)
    except Exception, inst:
       print "Unexpected error opening %s: %s" % (input_file, inst)
       import sys
       sys.exit(1)
    return tree

class Pair(object):
    def __init__(self, id, text, hypothesis, entailment, task):
        self.id = id
        self.text = text
        self.hypothesis = hypothesis
        self.entailment = entailment
        self.task = task

    def __repr__(self):
        return " ".join(["Pair<", str(self.id), str(self.task),
                         str(self.entailment), ">"])

class Sentence(object):
    def __init__(self, serial, terms):
        self.serial = serial
        self.terms = terms
    def __len__(self):
        return len(self.terms)

class Term(object):
    def __init__(self, id, word, pos, relation, lemma, idf=None):
        self.id = id
        self.word = word
        self.pos = pos
        self.relation = relation
        self.lemma = lemma
        self.idf = idf

#def todict(obj, classkey=None):
#    if isinstance(obj, dict):
#        for k in obj.keys():
#            obj[k] = todict(obj[k], classkey)
#        return obj
#    elif hasattr(obj, "__iter__"):
#        return [todict(v, classkey) for v in obj]
#    elif hasattr(obj, "__dict__"):
#        data = dict([(key, todict(value, classkey)) 
#            for key, value in obj.__dict__.iteritems() 
#            if not callable(value) and not key.startswith('_')])
#        if classkey is not None and hasattr(obj, "__class__"):
#            data[classkey] = obj.__class__.__name__
#        return data
#    else:
#        return obj
