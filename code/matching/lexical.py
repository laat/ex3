#coding=utf-8
"""
lexical matching, part 1 in the exercice
"""

from collections import defaultdict
from idf import idf

def number_match(tree, **kwargs):
    def _match(hypothesis, numbers_text):
        for sentence in hypothesis:
            for term in sentence.terms:
                if term.word:
                    try:
                        if not int(term.word) in numbers_text:
                            return False
                    except ValueError:
                        pass
        return True

    classes = []
    for pair in tree:
        numbers_text = {}
        for sentence in pair.text:
            for term in sentence.terms:
                if term.word:
                    try:
                        numbers_text[int(term.word)] = True
                    except ValueError:
                        pass
        score = _match(pair.hypothesis, numbers_text)
        classes.append((int(pair.id), score))
    return classes

def word_match(tree, idf_enabled=False, **kwargs):
    print "Doing word matching"
    classification = []
  
    for pair in tree:
        words = {}
        # initialize words
        hypothesis_lenght = 0
        for sentence in pair.hypothesis:
            for term in sentence.terms:
                if term.word:
                    if idf_enabled:
                        words[term.word] = 0
                        hypothesis_lenght += idf[term.word]
                    else:
                        words[term.word] = 0
                        hypothesis_lenght += 1

        # match words
        for sentence in pair.text:
            for term in sentence.terms:
                if term.word:
                    if term.word in words: 
                        if idf_enabled:
                            words[term.word] = idf[term.word]
                        else:
                            words[term.word] = 1

        # Normalize
        score = sum(words.values())/float(hypothesis_lenght)

        classification.append((int(pair.id), score))

    return classification

talla = [3,13,15,19,32,59,63,129,142,153,155,166,167,174,262,266,298,308,314,322,336,358,360,387,404,410,451,463,464,472,484,506,521,538,553,561,563,571,581,660,663,692,693,716,722,739,755]
nye_talla = [346,716,298,125,137,701,249,187,663,136,381,732,630,463,51,753,725,46]

def lemma_match(tree, pos=True, **kwargs):
    '''
        pos = use pos 
    '''
    print "Doing lemma matching"
    classes = []
 
    for pair in tree:
        lemmas = {}
        for sentence in pair.text:
            #if int(pair.id) in nye_talla:
            #    print "ID",pair.id,"|",pair.text,"|",pair.hypothesis
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
                        if pos: 
                            if term.pos in lemmas[term.lemma]: 
                            #ignoring pos gives better matching
                                matches += 1
                        else:
                            matches += 1

        score = matches/float(hypothesis_lenght)

        classes.append((int(pair.id), score))

    return classes

def get_simple_negations(tree):
    print "simple negation count"

    def _count_sentence(sentence):
        count = 0
        for term in sentence.terms:
            if term.relation and term.relation[0] in ["neg"]:
                count += 1
            elif term.word and term.relation and\
                    term.relation[0] in ["'t"]:
                count += 1
        return count

    classes = []
    for pair in tree:
        text_count = 0
        for text in pair.text:
            text_count += _count_sentence(text)

        h_count = 0
        for h in pair.hypothesis:
            h_count += _count_sentence(h)

        score = h_count%2 == text_count%2
        classes.append((int(pair.id), score))
    return classes


def bleu(tree, n=4, idf_enabled=False, return_only_n=False, lemma=False, **kwargs):
    print "Applying BLEU algorithm"
    classes = []
    for pair in tree:
        precn = [0]*n

        for i in xrange(n):
            precn[i] = get_precn(pair, i+1, lemma=lemma)

        if return_only_n:
            score = precn[return_only_n-1] * (1/float(n))
        else:
            score = sum(precn) * (1/float(n))

        classes.append((int(pair.id), score))
    return classes

def get_precn(pair,n, lemma=False):
    ngrams = {}
    ngram_length = 0
    for sentence in pair.hypothesis:
        gen = _generate_ngram_lemma(sentence, n) if lemma else _generate_ngram(sentence, n)
        for ngram in gen:
            ngram_length += 1
            if len(ngram):
                ngram = " ".join(ngram)
                ngrams[ngram] = 0

    #count
    for sentence in pair.text:
        gen = _generate_ngram_lemma(sentence, n) if lemma else _generate_ngram(sentence, n)
        for ngram in gen:
            ngram = " ".join(ngram)
            if ngram in ngrams:
                ngrams[ngram] += 1

    count = sum(ngrams.values())
    return count/float(ngram_length)

def _generate_ngram(sentence, n):
    for i in xrange(len(sentence)-n+1):
        words = [term.word for term in sentence.terms if term.word and term.word != "fin"]
        ngram = words[i:i+n]
        yield ngram

def _generate_ngram_lemma(sentence, n):
    for i in xrange(len(sentence)-n+1):
        words = [term.lemma for term in sentence.terms if term.lemma and term.lemma != "fin"]
        ngram = words[i:i+n]
        yield ngram
