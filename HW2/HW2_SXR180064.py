# NetID: sxr180064
# CS4395 - Mazidi
# HW2

import sys
import os
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from random import seed, randint

# Read input file
def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

# Calculate lexical diversity
def calculateLexicalDiversity(data):
    words = word_tokenize(data)
    lexicalDiversity = len(set(words)) / len(words)
    formattedLexicalDiversity = "{:.2%}".format(lexicalDiversity)
    return formattedLexicalDiversity

# Preprocess data
def preprocess(data):
    # Filter out stopwords and words below 6 letters
    tokens = [t.lower() for t in word_tokenize(data) if t.isalpha()]
    stopwordsEN = stopwords.words('english')
    filteredTokens = [t for t in tokens if t not in stopwordsEN and len(t) > 5]
    
    # Get unique lemmas
    wnl = WordNetLemmatizer()
    lemmatized = list(set([wnl.lemmatize(t) for t in filteredTokens]))

    # Perform part of speech tagging
    tags = nltk.pos_tag(lemmatized)
    print("First 20 tagged: {tagged}\n".format(tagged=tags[0:20]))

    # Get nouns and return filtered tokens + nouns
    nounLemmas = [lemma[0] for lemma in tags if lemma[1] == 'NN']
    print("Number of tokens: {numTokens}\n".format(numTokens=len(filteredTokens)))
    print("Number of nouns: {numNouns}\n".format(numNouns=len(nounLemmas)))
    return filteredTokens, nounLemmas

# Get 50 nouns with highest occurences
def getTopNouns(nounLemmas, tokens):
    # Count, sort and then return nouns
    nounCount = {}
    for noun in nounLemmas:
        nounCount[noun] = tokens.count(noun)
    top50 = {noun: count for noun, count in sorted(nounCount.items(), key=lambda nounNum: nounNum[1], reverse=True)[0:50]}
    print("Top 50 Nouns & Counts: {nounsToPrint}\n".format(nounsToPrint=top50))
    return [noun for noun in top50.keys()]

# Guessing game function
def guessingGame(wordBank):
    # Pre-game initialization
    print("\n\nLet's play a word guessing game!\n")
    points = 5
    guessed = True
    # Correct character guesses
    correctGuesses = []
    # Incorrect character guesses
    incorrectGuesses = []
    word = ""
    seed(1234)

    # Loop to play until points run out
    while points >= 0:
        # Reset word if guessed
        if guessed:
            word = wordBank[randint(0,49)]
            correctGuesses = []
            incorrectGuesses = []
            guessed = False
        
        # Generate string to show ("_" for unguessed and guessed characters)
        guessToShow = ""
        for char in word:
            if char in correctGuesses:
                guessToShow += char + " "
            else:
                guessToShow += "_ "
        
        # Show user guesses which failed along with current game status
        if len(incorrectGuesses) > 0: print("Failed Guesses: {failed}".format(failed=incorrectGuesses))
        print(guessToShow)

        # Detect if word has been guessed and start over
        if "_" not in guessToShow:
            print("Congratulations! You have solved this word.")
            print("\nGuess another word.\n")
            guessed = True
            continue
        
        # Get user input
        userInput = input("Guess a letter: ")
        # Quit upon "!"
        if userInput == "!":
            print("Exiting game...")
            return 0
        # Handle bad input
        elif not userInput.isalpha():
            print("Input is not a letter. Please guess a letter.\n")
        # Check if user already guessed the character
        elif userInput in incorrectGuesses:
            print("You have already guessed this. Please enter a new character.\n")
        # If user guesses correctly
        elif userInput in word:
            points += 1
            correctGuesses.append(userInput)
            print("Correct! Score is {score}\n".format(score=points))
        # If user guesses incorrectly
        else:
            points -= 1
            incorrectGuesses.append(userInput)
            print("Sorry, guess again. Score is {score}\n".format(score=points))
    
    # Game over + show user correct word
    print("You have run out of guesses.")
    print("The word was: {word}".format(word=word))
    print("Game over.")

# Driver function
if __name__ == '__main__':

    # Check for proper script invocation
    if len(sys.argv) < 2:
        print("Please provide directory to data file.")
        sys.exit()
    
    # Get input file contents
    fp = sys.argv[1]
    data = readFile(fp)
    # Print lexical diversity
    print("Lexical Diversity: {lexDiv}\n".format(lexDiv=calculateLexicalDiversity(data)))
    # Preprocess data
    tokens, nounLemmas = preprocess(data)
    # Get top 50 nouns to use for wordbank
    topNouns = getTopNouns(nounLemmas, tokens)
    # Star guessing game using generated workbank
    guessingGame(topNouns)