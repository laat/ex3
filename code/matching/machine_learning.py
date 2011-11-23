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


    #lemma_matching
    score = lexical.lemma_match(lexical_tree)
    for k, v in score:
        features[k].append(v)

    #bigram_matching (lemma)
    score = lexical.bleu(lexical_tree, n=2, return_only_n=2,
                         idf_enabled=idf_enabled, lemma=True)
    for k, v in score:
        features[k].append(v)

    #leamma_pos_matching
    score = lexical.lemma_match(lexical_tree)
    for k, v in score:
        features[k].append(v)

    #simple negation
    score = lexical.get_simple_negations(lexical_tree)
    for k, v in score:
        features[k].append(v)

    score = syntactic.tree_edit_distance(syntax_tree)
    for k,v in score:
        features[k].append(v)

    #appending task and entailment
    for k,v in features.iteritems():
        features[k].extend(ref[str(k)])

    return features

def write_features(outfile, features):
    ids = [int(k) for k in features.iterkeys()]
    ids.sort()
    with open(outfile, "w") as f:
        attribute = [("word", "c"), ("lemma","c"), ("lemmapos","c"), 
                     ("bigram", "c"), ("neg", "d"),  ("editdist","c"), ("task", "d"), ("stemmer", "d")]

        labels = [v[0] for v in attribute]
        datatype = [v[1] for v in attribute]
        f.write("\t".join(labels)+"\n")
        f.write("\t".join(datatype)+"\n")
        f.write("\t"*(len(labels)-1) + "class\n")
        for k in ids:
            v = features[k]
            f.write("\t".join(map(str, v))+"\n")

def knn_classifier(tree, outfile="dev.tab", **kwargs):
    import orange, orngTest
    classes = []
    # TODO: skipp skriving til fil
    outfile = outfile.rsplit(".",1)[0]
    data = orange.ExampleTable(outfile)

    knn = orange.kNNLearner(data, k=1, name="knn")
  
    for i, example in enumerate(data, 1):
        p = apply(knn, [example, orange.GetProbabilities])["YES"]
        classes.append((i, p))
    return classes

def knn_classifier_xv(tree, outfile="dev.tab", **kwargs):
    import orange, orngTest, orngStat
    classes = []
    # TODO: skipp skriving til fil
    outfile = outfile.rsplit(".",1)[0]
    data = orange.ExampleTable(outfile)

    knn = orange.kNNLearner(k=21, name="knn")

    results = orngTest.crossValidation([knn], data, folds=10)

    # output the results
    print "Learner  CA     IS     Brier    AUC"

    print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (knn.name, \
        orngStat.CA(results)[0], orngStat.IS(results)[0],
        orngStat.BrierScore(results)[0], orngStat.AUC(results)[0])

    print results.results[0].probabilities
    for i, example in enumerate(results.results, 1):
        p = example.probabilities[0]
        classes.append((i, p[1]))
    return classes

