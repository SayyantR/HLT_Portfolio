import os
import pickle

from nltk import word_tokenize
from nltk.util import ngrams

def processFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    text_in = text_in.replace('\n', ' ').replace('\r', ' ')

    unigrams = word_tokenize(text_in)
    bigrams = list(ngrams(unigrams, 2))

    unigramsDict = {t:unigrams.count(t) for t in set(unigrams)}
    bigramsDict = {b:bigrams.count(b) for b in set(bigrams)}

    return unigramsDict, bigramsDict

if __name__ == '__main__':
    
    unigramsDictEN, bigramsDictEN = processFile('./data/LangId.train.English')
    unigramsDictFR, bigramsDictFR = processFile('./data/LangId.train.French')
    unigramsDictIT, bigramsDictIT = processFile('./data/LangId.train.Italian')

    pickle.dump(unigramsDictEN, open('./pickles/unigramsEN.p', 'wb'))
    pickle.dump(bigramsDictEN, open('./pickles/bigramsEN.p', 'wb'))
    pickle.dump(unigramsDictFR, open('./pickles/unigramsFR.p', 'wb'))
    pickle.dump(bigramsDictFR, open('./pickles/bigramsFR.p', 'wb'))
    pickle.dump(unigramsDictIT, open('./pickles/unigramsIT.p', 'wb'))
    pickle.dump(bigramsDictIT, open('./pickles/bigramsIT.p', 'wb'))

    print("Unigram & Bigram generation completed.")