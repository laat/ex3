# coding=utf-8
from matching.lexical import word_match
from matching.lexical import lemma_match
from utils.classification import write
from utils.classification import find_best_threshold
from utils import load_xml
from eval_rte import evaluate

import argparse


METHODS = {
    "word": word_match,
    "lemma": lemma_match
}

def main(tree, output, method, threshold, find_best):
    # funky case switch

    if find_best:
        find_best_threshold(tree[0], METHODS[method], tree[1], output)
    else:
        classification = METHODS[method](tree[0], threshold=threshold)
        print "writing output"
        write(classification, output)
        print "Accuracy = %.4f" % evaluate(tree[1], output)
        
class InputFileAction(argparse.Action):
        # Kalles når inputfile er satt, inputfil blir en liste av par, isteden
        # for pathen til input_file
    def __call__(self, parser, namespace, values, option_string=None):
        print "Parsing xml-file..."
        val = load_xml.get_pairs(values)
        print "done."
        setattr(namespace, self.dest, (val, values))

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--input_file", dest="tree", type=str,
                            action=InputFileAction, required=True)
        parser.add_argument("-o", "--output_file", dest="output", type=str,
                            required=True)
        parser.add_argument('-m', '--method', type=str, required=True, 
                            choices=METHODS.keys())
        parser.add_argument('-t', '--threshold', type=float, default=0.4)
        parser.add_argument('-b', '--find_best_threshold', action='store_true')
        args = parser.parse_args()


        args = vars(args)
        main(
            args['tree'],
            args['output'],
            args['method'],
            args['threshold'],
            args['find_best_threshold']
        )
