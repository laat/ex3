#coding=utf-8
"""
writes classification in the correct format
"""

from eval_rte import evaluate
from eval_rte import parse_reference


def find_best_threshold(tree, method, input_file, output_file, n=4, idf_enabled=False):
    results = method(tree, n=n, idf_enabled=idf_enabled)
    reference = parse_reference(input_file)  # some speedup, read once

    best_threshold = 0.01
    best_accuracy = 0
    threshold = 0.01
    while(threshold <= 1):
        threshold = round(threshold,2)
        classification = classify_results(results, threshold) 
        #write(classification, output_file)
        #find accuracy
        acc = evaluate(input_file, output_file, pred_id2label=classification, ref_id2label=reference)
        print "th:", threshold, "acc:",acc
        if acc >= best_accuracy:
            best_threshold = threshold
            best_accuracy = acc
        threshold += 0.01
    print "best threshold was %.2f with %.4f accuracy" % (best_threshold,
                                            best_accuracy)

def classify_results(results, threshold):
    res = {}
    for r in results:
        if r[1] > threshold:
            res[str(r[0])] = "YES"
        else:
            res[str(r[0])] = "NO"
    return res

def write(classifications, output_file):
    classifications = [(k,v) for k,v in classifications.iteritems()]

    strings = ["ranked: no\n"]
    classifications.sort()
    for classification in classifications:
        strings.append(str(classification[0]) + " "+classification[1] + "\n")

    with open(output_file, "w") as f:
        f.writelines(strings)
