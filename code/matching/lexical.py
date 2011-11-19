#coding=utf-8
"""
lexical matching, part 1 in the exercice
"""

from collections import defaultdict

def word_match(tree, threshold=0.4):
    print "Doing word matching"
    classification = []
    for pair in tree:
        words = {}
        # initialize words
        for sentence in pair.text:
            for term in sentence.terms:
                if term.word:
                    words[term.word] = 0

        hypothesis_lenght = 0
        # match words
        for sentence in pair.hypothesis:
            hypothesis_lenght += len(sentence)
            for term in sentence.terms:
                if term.word:
                    if term.word in words:
                        words[term.word] = 1

        # Normalize
        score = sum(words.values())/float(hypothesis_lenght)

        result = False
        if threshold < score:
            result = True

        classification.append((int(pair.id), result))

    return classification

def lemma_match(tree, threshold=0.4):
    print "Doing lemma matching"
    classes = []
    for pair in tree:

        lemmas = {}
        for sentence in pair.text:
            for term in sentence.terms:
                if term.word and term.lemma and term.pos:
                    if not term.lemma in lemmas: #initalize var
                        lemmas[term.lemma] = {term.pos: 0}
                    else:
                        lemmas[term.lemma][term.pos] = 0
        matches = 0
        hypothesis_lenght = 0
        #matching lemma and pos
        for sentence in pair.hypothesis:
            hypothesis_lenght += len(sentence)
            for term in sentence.terms:
                if term.word and term.lemma and term.pos:
                    if term.lemma in lemmas:
                        #if term.pos in lemmas[term.lemma]: 
                        #ignoring pos gives better matching
                            matches += 1

        score = matches/float(hypothesis_lenght)

        result = False
        if threshold < score:
            result = True

        classes.append((int(pair.id), result))

    return classes


# BLEU
def bleu(tree, threshold=0.4, n=4):
    print "Applying BLEU algorithm"
    classes = []
    for pair in tree:
        precn = [0]*n

        for i in xrange(n):
            precn[i] = get_precn(pair, i+1)
        score = sum(precn) * (1/float(n))

        result = False
        if threshold < score:
            result = True

        classes.append((int(pair.id), result))
    return classes

def get_precn(pair,n):
    ngrams = {}
    ngram_length = 0
    for sentence in pair.hypothesis:
        for ngram in _generate_ngram(sentence, n):
            ngram_length += 1
            if len(ngram):
                ngram = " ".join(ngram)
                ngrams[ngram] = 0

    #count
    for sentence in pair.text:
        for ngram in _generate_ngram(sentence, n):
            ngram = " ".join(ngram)
            if ngram in ngrams:
                ngrams[ngram] += 1
    count = sum(ngrams.values())

    return count/float(ngram_length)

def _generate_ngram(sentence, n):
    for i in xrange(len(sentence)-n+1):
        words = [term.word for term in sentence.terms if term.word and term.word != "."]
        ngram = words[i:i+n]
        yield ngram
