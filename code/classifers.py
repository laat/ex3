# Description: Demostration of use of cross-validation as provided in orngEval module
# Category:    evaluation
# Uses:        voting.tab
# Classes:     orngTest.crossValidation
# Referenced:  c_performance.htm

import orange, orngTest, orngStat, orngTree, orngFSS,orngDisc

# set up the learners
bayes = orange.BayesLearner()
majority = orange.MajorityLearner()
tree = orngTree.TreeLearner(mForPruning=2)
#tree = orngTree.TreeLearner(sameMajorityPruning=1, mForPruning=2)
knn = orange.kNNLearner(k=21)
c = orange.C45Learner(minObjs=100)

bayes.name = "bayes"
tree.name = "tree"
majority.name = "majority"
knn.name = "knn"
c.name = "C45"

learners = [bayes, tree, majority, knn, c]

# compute accuracies on data
data = orange.ExampleTable("train")
results = orngTest.crossValidation(learners, data, folds=10)

print len(results.results)
for tested in results.results:
    print tested.iterationNumber, tested.classes, tested.actualClass

print dir(results)

# output the results
print "Learner  CA     IS     Brier    AUC"
for i in range(len(learners)):
    print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, \
        orngStat.CA(results)[i], orngStat.IS(results)[i],
        orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])

def report_relevance(data):
    m = orngFSS.attMeasure(data)
    for i in m:
        print "%5.3f %s" % (i[1], i[0])

print
print "relevans"
report_relevance(data)

