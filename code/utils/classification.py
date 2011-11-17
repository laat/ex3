#coding=utf-8
"""
writes classification in the correct format
"""

from eval_rte import evaluate

def write(classifications, output_file):
    strings = ["ranked: no\n"]
    classifications.sort()
    for classification in classifications:
        result = " YES" if classification[1] else " NO"
        strings.append(str(classification[0]) + result + "\n")

    with open(output_file, "w") as f:
        f.writelines(strings)

def find_best_threshold(tree, method, input_file, output_file):
    best_threshold = 0.05
    best_accuracy = 0
    threshold = 0.05
    while(threshold <= 1):
        #classify with thresshold
        classification = method(tree, threshold=threshold)
        write(classification, output_file)

        #find accuracy
        acc = evaluate(input_file, output_file)
        print "th:", threshold, "acc:",acc
        if acc >= best_accuracy:
            best_threshold = threshold
            best_accuracy = acc

        threshold += 0.05
    print "best threshold was %.2f with %.4f accuracy" % (best_threshold,
                                            best_accuracy)
