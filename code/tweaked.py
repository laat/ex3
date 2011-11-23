#coding=utf-8
import argparse
from utils.classification import classify_results
from utils.classification import write
from matching.tweaked import tweaked_on_testdata
from matching.tweaked import get_features
from matching.tweaked import tweaked
from matching.tweaked import write_f
from eval_rte import evaluate
from matching.machine_learning import write_features

def main(training_data, test_data, output_file):
    if test_data:
        training_features = get_features(training_data)
        test_features = get_features(test_data)

        write_features("train.tab", training_features)
        write_features("test.tab", test_features)
        results = tweaked_on_testdata("train.tab", "test.tab")
        classification = classify_results(results, 0.5) 

        print "witing output"
        write(classification, output_file)
    else:
        training_features = get_features(training_data)
        write_f("train.tab", training_features)
        results = tweaked("train.tab") # cross-validation

        print "classifying"
        classification = classify_results(results, 0.5) 
        print "writing output"
        write(classification, output_file)

        print "Accuracy = %.4f" % evaluate(training_data, output_file)

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--training_data", type=str,
                            required=True)
        parser.add_argument("-t", "--test_data", type=str)
        parser.add_argument("-o", "--output_file", type=str,
                            required=True)

        args = vars(parser.parse_args())
        main(
            args["training_data"],
            args["test_data"],
            args["output_file"]
        )
