# coding=utf-8
from matching.lexical import word_match
from matching.lexical import lemma_match
from matching.lexical import bleu
from matching.syntactic import print_tree_edit_distance
from matching.syntactic import tree_edit_distance
from matching.idf import generate_idf_score
from utils.tree_edit_distance import postorder
from utils.classification import write
from utils.classification import classify_results
from utils.classification import find_best_threshold
from utils import load_xml
from utils import create_tree
from eval_rte import evaluate

import argparse
import pickle


# funky case switch with METHODS
METHODS = {
    "word": word_match,
    "lemma": lemma_match,
    "bleu": bleu,
    "print_ted": print_tree_edit_distance,
    "ted" : tree_edit_distance
}

def main(tree, output, method, threshold, find_best, n=4, idf_enabled=False):
    # first phase, loading file
    print "Loading xmlfile"
    if method in ["word", "lemma", "bleu"]:
        tree = (load_xml.get_pairs(tree), tree)
    else:
        tree = (create_tree.generate_syntax_tree(tree), tree)
    print "done."



    if idf_enabled:
        if method in ["ted", "print_ted"]:
            ## using another treestructure, must generate it for this method
            generate_idf_score(load_xml.get_pairs(tree[1]))
        else:
            generate_idf_score(tree[0])

    if find_best:
        find_best_threshold(tree[0], METHODS[method], tree[1], 
                            output, n=n, idf_enabled=idf_enabled)
    else:
        results = METHODS[method](tree[0], n=n, idf_enabled=idf_enabled)
        classification = classify_results(results, threshold) 

        print "writing output"
        write(classification, output)
        print "Accuracy = %.4f" % evaluate(tree[1], output)
        
if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--input_file", dest="file", type=str)
        parser.add_argument("-o", "--output_file", dest="output", type=str,
                            required=True)
        parser.add_argument('-m', '--method', type=str, required=True, 
                            choices=METHODS.keys())
        parser.add_argument('-t', '--threshold', type=float, default=0.4)
        parser.add_argument('-n', '--ngram_length', type=int, default=3)
        parser.add_argument('-b', '--find_best_threshold', action='store_true')
        parser.add_argument('-i', '--idf_enabled', action='store_true')
        args = parser.parse_args()


        args = vars(args)
        main(
            args['file'],
            args['output'],
            args['method'],
            args['threshold'],
            args['find_best_threshold'],
            n = args["ngram_length"],
            idf_enabled = args['idf_enabled']
        )
