# -*- coding: utf-8 -*-
"""HW3_SXR180064.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wH7csMUPaDb38wImo_zgKeHvwOy7kWQ0

# HW3 - WordNet
Name: Sayyant Rath

Class: CS 4395.001

WordNet is essentially a databse of words which are linked by semantic relations such as synonyms, hyponyms, etc. The groups are known as synsets including short definitions and example usages.
"""

import nltk
nltk.download('all')

import math
import itertools
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.wsd import lesk
from nltk.book import *
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)
                if type(ngram) == tuple])

def getSynsetInfo(ss):
  print("Synset to use: {sset}\n".format(sset=ss))

  # Extract definitions
  definition = ss.definition()
  print("Definition: {definition}".format(definition=definition))
  # Extract usages
  usages = ss.examples()
  print("Usages: {usages}".format(usages=usages))
  # Rxtract lemmas
  lemmas = ss.lemmas()
  print("Lemmas: {lemmas}".format(lemmas=lemmas))

  # Traverse the WordNet hierarchy
  hyper = lambda s: s.hypernyms()
  hierarchy = list(ss.closure(hyper))
  print("\nHierarchy:")
  print(hierarchy)

  if ss.pos() == 'n':
    # Extract hypernyms
    hypernyms = ss.hypernyms()
    print("\nHypernyms: {hypernyms}".format(hypernyms=hypernyms))
    # Extract homonyms
    hyponyms = ss.hyponyms()
    print("Hyponyms: {hyponyms}".format(hyponyms=hyponyms))
    # Extract meronyms
    meronyms = ss.part_meronyms()
    print("Meronyms: {meronyms}".format(meronyms=meronyms))
    # Extract meronyms
    holonyms = ss.part_holonyms()
    print("Holonyms: {holonyms}".format(holonyms=holonyms))
    # Extract antonyms
    antonyms = lemmas[0].antonyms()
    print("Antonyms: {antonyms}".format(antonyms=antonyms))

# Getting all synsets of the noun "car"
car = wn.synsets('airplane')
print("Synsets for the word 'car':")
car

# Getting synset information for first noun synset of the noun "car" (Steps 2 - 4)
getSynsetInfo(car[0])

"""It seems that the nouns in WordNet are organized using an "is a" kind of relationship. For example, "think" is a "deliberation" which is a "consideration" and if we consider it at a larger scale, "think" is a "psychologocial feature." This relationship is described as a hypernym which is used to create the heirarchy that WordNet is structured with."""

# Getting all synsets of the verb "think"
think = wn.synsets('think')
print("Synsets for the word 'think':")
think

# Getting synset information for first verb synset of the verb "think" (Steps 5 & 6)
getSynsetInfo(think[1])

# Using Morphy to find different forms of "think"

print("Verb: {verb}".format(verb=wn.morphy('think', wn.VERB)))
print("Noun: {noun}".format(noun=wn.morphy('think', wn.NOUN)))
print("Adverb: {adverb}".format(adverb=wn.morphy('think', wn.ADV)))
print("Adjective: {adjective}".format(adjective=wn.morphy('think', wn.ADJ)))

# Running the Wu-Palmer Similarity Metric and the Lesk Algorithmon two words
print("Two words which might be similar: 'airplane' & 'airport'")

# Getting synsets
airplane = wn.synsets('airplane')
ss1 = airplane[0]

airport = wn.synsets('airport')
ss2 = airport[0]

# Getting Wu-Palmer Results
print("Wu-Palmer Similarity Metric: {metric}".format(metric = wn.wup_similarity(ss1, ss2)))

# Getting Lesk results
print("Lesk Algorithm Results: {leskRes}".format(leskRes= lesk(['airplane'], 'airport')))

"""### Wu-Palmer Similarity Metric & Lesk Algorithm

The Wu-Palmer similarity metric is a metric used in NLP to determine two words' similarity to each other using the semantic relationship in a lexical database such as WordNet. The Lesk Algorithm is a word disambiguation technique used to compare the words in context of a target word with the words in the definitions of each of the word's senses where the sense possessing the highest overlap with the context word is chosen.

### SentiWordNet

SentiWordNet is another lexical resource which can be used for opinion mining and sentiment analysis. It is also a lexical database which maps sentiment scores to words based off of te semantical orientation of the word which can then be used to determine the sentiment of text in NLP.
"""

# Getting Sentisynsets of the word "Catastrophe"
horrified = list(swn.senti_synsets("catastrophe"))
print("SentiSynSets for 'Catastrophe' and polarity scores:")
for item in horrified:
  print(item)

# Analyzing the sentiment of the sentence "I do not especially appreciate presents"
sentence = "I do not especially appreciate big presents"
print("\nAnalyzing the sentence 'I do not especially appreciate presents':")
neg = 0
pos = 0
tokens = sentence.split(" ")
for token in tokens:
  synList = list(swn.senti_synsets(token))
  if synList:
      syn = synList[0]
      neg += syn.neg_score()
      pos += syn.pos_score()
print("Positive score: {pos}".format(pos=pos))
print("Negative score: {neg}".format(neg=neg))
if pos > neg:
  print("Positiive sentiment")
elif neg > pos:
  print("Negative sentiment")
else:
  print("Neutral sentiment")

"""In the sentence I provided, the scores were generally negative which is accurate but the approach tho scoring was flawed in several ways. For example, the sentisynsets of 'I' could be referring to the word 'iodine,' 'one,' or 'I.' As such, simply using the first synset could lead to innacurate scoring. Keeping track of these scores allows us to ascribe context to the data that each word has. Nevertheless, selecting the most relevant synset is also necessary to ensure accuracy of the scores though as the text gets larger, this issue becomes less apparent.

### Colocations

A colocation is a series of words which appears frequently throughout a piece of text. They can be thought of as a set of words with a fixed meaning which is important to the understanding of the text. They can be identified using statistical techniques such as frequency analysis and association measures like pointwise mutual information (PMI).
"""

# Getting colocations for text4
collocations = bigram_word_feats(text4)
wordToUse = " ".join(list(collocations.keys())[5])

text = ' '.join(text4.tokens)
vocab = len(set(text4))
hg = text.count(wordToUse)/vocab
h = text.count('BUSINESS')/vocab
g = text.count('COOPERATION')/vocab
pmi = math.log2(hg / (h * g))
print('pmi = ', pmi)
hg = text.count('of the')/vocab
print("p(of the) = ",hg )
o = text.count('of')/vocab
print("p(of) = ", o)
t = text.count('the ')/vocab # space so it doesn't capture 'their' etc.
print('p(the) = ', t)
pmi = math.log2(hg / (o * t))
print('pmi = ', pmi)