import pickle
import os

from nltk import word_tokenize
from nltk.util import ngrams

def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

def compute_prob(text, unigram_dict, bigram_dict, V):

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    
    p_laplace = 1

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace

if __name__ == '__main__':
    unigramsEN = pickle.load(open('./pickles/unigramsEN.p', 'rb'))
    unigramsFR = pickle.load(open('./pickles/unigramsFR.p', 'rb'))
    unigramsIT = pickle.load(open('./pickles/unigramsIT.p', 'rb'))
    bigramsEN = pickle.load(open('./pickles/bigramsEN.p', 'rb'))
    bigramsFR = pickle.load(open('./pickles/bigramsFR.p', 'rb'))
    bigramsIT = pickle.load(open('./pickles/bigramsIT.p', 'rb'))

    data = readFile('./data/LangId.test')
    lineDelimittedData = data.split("\n")

    results = []
    resFile = open("./data/wordLangId.out", "w")

    for line in lineDelimittedData:
        p_EN = compute_prob(line, unigramsEN, bigramsEN, len(unigramsEN))

        p_FR = compute_prob(line, unigramsFR, bigramsFR, len(unigramsFR))

        p_IT = compute_prob(line, unigramsIT, bigramsIT, len(unigramsIT))

        language = max([p_EN, p_FR, p_IT])

        if language == p_EN:
            results.append("English")
            resFile.write("English\n")
        elif language == p_FR:
            results.append("French")
            resFile.write("French\n")
        else:
            results.append("Italian")
            resFile.write("Italian\n")
    
    solution = readFile('./data/LangId.sol')
    solution = solution.split("\n")[:-1]
    solution = [line.split(" ")[1] for line in solution]

    score = 0
    incorrectLines = []

    for i in range(len(solution)):
        if solution[i] == results[i]:
            score += 1
        else:
            incorrectLines.append(i + 1)
    
    print("Accuracy of model: {score}%".format(score=score/len(solution)*100))
    print("Incorrect Lines: {incorrectLines}".format(incorrectLines=incorrectLines))
    resFile.close()
