#coding=utf-8
"""
lexical matching, part 1 in the exercice
"""

from collections import defaultdict

def word_match(tree, threshold=0.4):
    print "Doing word matching"
    classification = []
    for pair in tree:
        #words = defaultdict(int)  # dict som returnerer 0 når key ikke finnes
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
