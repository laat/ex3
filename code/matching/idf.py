#coding = utf-8
from collections import defaultdict
from math import log

idf = {}

def generate_idf_score(tree):
    print "Calculating idf scores"
    global idf
    n, df = count_words_in_documtents(tree)

    for word, freq in df.iteritems():
        idf[word] = log(n/freq)

def count_words_in_documtents(tree):
    n_documents = 0 
    document_frequency = defaultdict(int)
    for pair in tree:
        words = set()

        for sentence in pair.text:
            for term in sentence.terms:
                if term.word:
                    words.add(term.word)

        for sentence in pair.hypothesis:
            for term in sentence.terms:
                if term.word:
                    words.add(term.word)

        for w in words:
            document_frequency[w] += 1
        
        n_documents += 1

    return n_documents, document_frequency
