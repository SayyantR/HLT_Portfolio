from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import random
import string
import re
import string
import unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import warnings
import openai
import spacy

spcy = spacy.load("en_core_web_sm")
warnings.filterwarnings("ignore")
nltk.download('punkt')
nltk.download('wordnet')

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

data = open('./data/space_exploration.txt')
raw = data.read()
raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw)

def Normalize(text):
    punct_dict = dict((ord(punct), None)
                             for punct in string.punctuation)
    word_token = nltk.word_tokenize(text.lower().translate(punct_dict))
    new_words = []
    for word in word_token:
        new_word = unicodedata.normalize('NFKD', word).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)

    rmv = []
    for w in new_words:
        text = re.sub("&lt;/?.*?&gt;", "&lt;&gt;", w)
        rmv.append(text)

    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    lemmatizer = WordNetLemmatizer()
    lemma_list = []
    rmv = [i for i in rmv if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = lemmatizer.lemmatize(token, tag_map[tag[0]])
        lemma_list.append(lemma)
    return lemma_list

def welcome(user_response):
    welcomes = ["hi", "hey", "hi there",
                    "hello",]
    for word in user_response.split():
        if word.lower() in welcomes:
            return random.choice(welcomes)


def answerQ(user_response):
    botresponse = ""
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(
        tokenizer=Normalize,
        stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0 or "ask via chatgpt" in user_response.lower()):
        print(user_response)
        response = openai.Completion.create(
            engine='text-davinci-002',
            prompt=user_response.split("ask via chatgpt: ")[-1],
            
        )
        resp = response["choices"][0]["text"]
        return resp
    else:
        botresponse = botresponse+sent_tokens[idx]
        return botresponse

user_data = {
    "Sean": {
        "likes": ["climbing", "mountain biking", "swimming", "reading"],
        "dislikes": ["movies", "amusement parks"],
        "misc.": []
    },
    "Ruby": {
        "likes": ["running", "coding", "photography"],
        "dislikes": ["pickles", "javascript"],
        "misc.": []
    }
}
    
asking = True
print("My name is SpaceBot and I'm a chatbot that knows about space exploration. If you want to exit, type exit. What is your name?")
user_info = input()
user = {}
if user_info in user_data.keys():
    user = user_data[user_info]
else:
    user_data[user_info] = {
        "likes": [],
        "dislikes": [],
        "misc.": []
    }
    user = user_data[user_info]
print("Nice to meet you!")

while (asking == True):
    user_response = input()
    user_response = user_response.lower()
    if (user_response not in ['exit', 'quit']):
        if (user_response == 'thanks' or user_response == 'thank you'):
            asking = False
            print("SpaceBot : You are welcome..")
        else:
            if (welcome(user_response) != None):
                print("SpaceBot : "+welcome(user_response))
            elif ("i " in user_response and "?" not in user_response):
                if "like" in user_response:
                    keywords = spcy(user_response)
                    user["likes"].append(keywords[-1])
                elif "dislike" or "not like" in user_response:
                    keywords = spcy(user_response)
                    user["dislikes"].append(keywords[-1])
                else:
                    print("SpaceBot : ", end="")
                    print(answerQ(user_response))
                    sent_tokens.remove(user_response)
            elif (" i " in user_response or " me " in user_response or " my " in user_response):
                if "like" in user_response:
                    print("you like:")
                    for like in user["likes"]: 
                        print(like)
                elif "dislike" or "not like" in user_response:
                    print("you dislike:")
                    for dislike in user["dislikes"]:
                        print(dislike)
                elif "name" in user_response:
                    print("Your name is: " + user_info)
                else:
                    print("SpaceBot : ", end="")
                    print(answerQ(user_response))
                    sent_tokens.remove(user_response)
            else:
                print("SpaceBot : ", end="")
                print(answerQ(user_response))
                sent_tokens.remove(user_response)
    else:
        asking = False
        print("Spacebot : Bye")
