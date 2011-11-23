#coding=utf-8
from matching.idf import generate_idf_score
from matching import lexical
from matching import syntactic
from utils import load_xml
from utils import create_tree
from eval_rte import parse_reference

from xml.etree.ElementTree import iterparse
from collections import defaultdict


def get_attributes_pair(in_file):
    features = {}
    for event, elem in iterparse(in_file):
        if elem.tag == "pair":
            features[elem.get("id")] = [elem.get("task"), elem.get("entailment")]
    return features

def get_entailment(in_file):
    features = {}
    for event, elem in iterparse(in_file):
        if elem.tag == "pair":
            features[elem.get("id")] = [elem.get("entailment")]
    return features

def get_features(in_file, idf_enabled=False):
    print "loading xml..."
    lexical_tree = load_xml.get_pairs(in_file)
    syntax_tree = create_tree.generate_syntax_tree(in_file)
    print "done loading"

    if idf_enabled:
        generate_idf_score(lexical_tree)

    print "parsing reference"
    ref = get_attributes_pair(in_file)

    print "extracting features"
    features = defaultdict(list)

    #word_matching
    score = lexical.word_match(lexical_tree, idf_enabled=idf_enabled)
    for k, v in score:
        features[k].append(v)


    #simple negation
    score = lexical.get_simple_negations(lexical_tree)
    for k, v in score:
        features[k].append(v)

    #tree edit distance
    score = syntactic.tree_edit_distance(syntax_tree)
    for k,v in score:
        features[k].append(v)

    #number_match
    score = lexical.number_match(lexical_tree)
    for k,v in score:
        features[k].append(v)

    #appending task and entailment
    for k,v in features.iteritems():
        features[k].extend(ref[str(k)])

    return features

def write_f(outfile, features):
    print "wtiting features"
    ids = [int(k) for k in features.iterkeys()]
    ids.sort()
    with open(outfile, "w") as f:
        attr = [("word", "c"),
                     ("neg", "d"),  
                     ("editdist","c"), 
                     ("numb", "d"), 
                     ("task", "d"), 
                     ("stemmer", "d")]

        labels = [v[0] for v in attr]
        datatype = [v[1] for v in attr]
        f.write("\t".join(labels)+"\n")
        f.write("\t".join(datatype)+"\n")
        f.write("\t"*(len(labels)-1) + "class\n")
        for k in ids:
            v = features[k]
            f.write("\t".join(map(str, v))+"\n")

def tweaked(outfile, **kwargs):
    import orange, orngTest
    classes = []

    outfile = outfile.rsplit(".",1)[0]
    data = orange.ExampleTable(outfile)

    c45 = orange.C45Learner(minObjs=100)

    results = orngTest.crossValidation([c45], data, folds=10)
    for i, example in enumerate(results.results, 1):
        p = example.probabilities[0]
        classes.append((i, p[1]))
    return classes

def tweaked_on_testdata(train_file, test_file, **kwargs):
    import orange, orngTest
    classes = []
    train_file = train_file.rsplit(".",1)[0]
    test_file = test_file.rsplit(".",1)[0]

    test_data = orange.ExampleTable(test_file)
    train_data = orange.ExampleTable(train_file)

    learner = orange.C45Learner(train_data, minObjs=100)

    for i, test in enumerate(test_data, 1):
        p = apply(learner, [test, orange.GetProbabilities])["YES"]
        classes.append((i, p))
    return classes
