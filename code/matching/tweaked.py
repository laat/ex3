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

    #1,2,3-gram with synonyms of lemmas 
    for n in [1,2,3]:
        score = bleu(lexical_tree, n=n, idf_enabled=True, lemma=True, synonyms=True)
        for k,v in score:
            features[k].append(v)

    memory = {}
    for n in [2,3]: # 2-gram without synonyms
        score = bleu(lexical_tree, n=n, idf_enabled=True, lemma=True, synonyms=False)
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
                     ("bleu1", "c"), 
                     ("bleu2" "c"), 
                     ("bleu3", "c"), 
                     ("bleu2s", "c"), 
                     ("bleu3s", "c"), 
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

    #c45 = orange.C45Learner(minObjs=100)
    c45 = orange.kNNLearner(minObjs=100)

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


####################33


def bleu(tree, n=4, idf_enabled=False, return_only_n=False, lemma=False, synonyms=False, **kwargs):
    memory = {}
    print "Applying BLEU algorithm"
    classes = []
    for pair in tree:
        precn = [0]*n

        for i in xrange(n):
            precn[i] = get_precn(pair, i+1, lemma=lemma, synonyms=synonyms)

        if return_only_n:
            score = precn[return_only_n-1] * (1/float(n))
        else:
            score = sum(precn) * (1/float(n))

        classes.append((int(pair.id), score))
    return classes


def get_precn(pair,n, lemma=False, synonyms=False):
    matching = 0
    total = 0

    for hyp in pair.hypothesis:
        for tex in pair.text:
            for i in range(0,len(hyp)-n+1):
                def _tmp():
                    for a in range(0,n+1):
                        if i+a >= len(hyp.terms) or i+a >= len(tex.terms): return False
                        term = hyp.terms[i+a]
                        other_term = tex.terms[i+a]
                        if not _memoized_term_equals(term, other_term, lemma=lemma, synonyms=synonyms): return False
                    return True
                if _tmp(): matching += 1
                total += 1
    return matching/float(total)


memory = {} # remember to reset!
def _get_synonyms(word):
    if word and word != "fin": 
        from nltk.corpus import wordnet as wn
        for ss in wn.synsets(word):
            for n in ss.lemma_names:
                yield n

def _term_equals(a,b,lemma=True,synonyms=True,use_pos=False):
    #if use_pos and a
    a_syns = _get_synonyms(a.lemma) if synonyms else [a.lemma]
    b_syns = set(_get_synonyms(b.lemma)) if synonyms else [b.lemma]
    for syn in a_syns:
        if syn not in b_syns: 
            return False
    return True

def _memoized_term_equals(a,b,lemma=True,synonyms=True,use_pos=False):
    try: return memory[a,b]
    except: pass
    b = _term_equals(a,b)
    memory[a,b] = b
    return b

