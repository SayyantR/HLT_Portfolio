from collections import defaultdict, Counter
import re
import os
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
import requests
import urllib.request
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import Error

F1_KEYWORDS = [
    'red-bull',
    'aston-martin',
    'mercedes',
    'ferrari',
    'alfa-romeo',
    'alpine',
    'williams',
    'alphatauri',
    'haas',
    'mclaren',
    'perez',
    'verstappen',
    'stroll',
    'alonso',
    'russell',
    'hamilton',
    'sainz',
    'leclerc',
    'guanyu',
    'bottas',
    'ocon',
    'sargeant',
    'albon',
    'de vries',
    'tsunoda',
    'magnusen',
    'hulkenberg',
    'piastri',
    'norris',
    'formula 1',
    'f1',
    'racing',
    'car',
    'fia',
    'grand prix',
    'race',
    'gp'
]

DISTRACTORS = [
    'google',
    'nascar',
    'pinterest',
    'facebook',
    'twitter',
    'instagram',
    'youtube',
    'linkedin',
    'calendar',
    'author'
]

def def_value():
    return 0

def getDomain(url):
    if 'www.' in url:
        return url.split(".")[1]
    else:
        return url.split("/")[2].split(".")[0]

def getURL(link):
    if link.startswith('/url?'):
        return link.split('&')[0][7:]
    elif link.startswith('https://'):
        return link
    return False

def isValid(url):
    httpsCheck = url.startswith('https://')
    wikiCheck = 'wiki' not in url
    fileCheck = 'files' not in url
    dupeCheck = 'archive' not in url
    newsCheck = '-' in url

    return httpsCheck and wikiCheck and fileCheck and dupeCheck and newsCheck

def getStoryIndex(link):
    index = 0
    for char in link:
        if char == '/': index += 1
        elif char == '-': return index

def isRelevant(link):
    isRelevant = False
    if len(list(filter(lambda keyword: keyword in link.lower(), F1_KEYWORDS))) > 0:
        if len(list(filter(lambda distractor: distractor in link.lower(), DISTRACTORS))) == 0:
            index = getStoryIndex(link)
            for word in link.split("/")[index].split("-"):
                ss = wn.synsets(word)
                if len(ss) > 0 and ss[0].pos() == 'v':
                    isRelevant = True
    return isRelevant

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def BFSWebScraper(url):
    queue = [url]
    validURLs = []
    domainCount = defaultdict(def_value)

    while len(queue) != 0 or len(validURLs) < 15:
        URLToVisit = queue.pop(0)
        html = requests.get(URLToVisit).text
        soup = BeautifulSoup(html)
        
        links = soup.find_all('a', href=True)
        links = [link['href'] for link in links]
        for link in links:
            if len(validURLs) >= 15: break
            newURL = getURL(link)
            if not newURL:
                continue
            if not isValid(newURL):
                continue
            if isRelevant(newURL):
                domain = getDomain(newURL)
                if domainCount[domain] >= 8: continue
                validURLs.append(newURL)
                queue.append(newURL)
                domainCount[domain] += 1
    
    return validURLs

def scrapeURLS(urls):
    for idx, url in enumerate(urls):
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html)
        data = soup.findAll(text=True)
        result = filter(visible, data)
        textList = list(result)
        text = ' '.join(textList)
        f = open("./raw_text/raw{idx}.txt".format(idx=idx), "w")
        f.write(text)
        f.close()

def clean():
    for i in range(0, 15):
        with open(os.path.join(os.getcwd(), "./raw_text/raw{i}.txt".format(i=i)), 'r') as f:
            text_in = f.read()
        text_in = text_in.replace('\n', ' ').replace('\r', ' ').replace("\t", ' ')
        sentences = sent_tokenize(text_in)
        f = open("./sentences/sentences{idx}.txt".format(idx=i), "w")
        for sentence in sentences:
            f.write(sentence)
        f.close()

def extract():
    allTokens = []
    for i in range(0, 15):
        with open(os.path.join(os.getcwd(), "./sentences/sentences{i}.txt".format(i=i)), 'r') as f:
            text_in = f.read()
        text_in = re.sub(r'[.?!,:;()\-\n\d]', ' ', text_in.lower())
        stopwordsEN = stopwords.words('english')
        tokens = [t.lower() for t in word_tokenize(text_in) if t.isalnum() and t not in stopwordsEN]
        allTokens.extend(tokens)
    counter = Counter(allTokens)
    return counter.most_common(50)

def getFacts(tokens):
    facts = {key:[] for key in tokens}
    for i in range(0, 15):
        with open(os.path.join(os.getcwd(), "./raw_text/raw{i}.txt".format(i=i)), 'r') as f:
            text_in = f.read()
        text_in = text_in.replace('\n', ' ').replace(
            '\r', ' ').replace("\t", ' ')
        sentences = sent_tokenize(text_in)
        for sentence in sentences:
            for token in tokens:
                if token in sentence.lower():
                    facts[token].append(sentence)
    return facts
        
    

def createKB(facts):
    try:
        connection = psycopg2.connect(user="sayyantrath",
                                    password="Portland21",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="kbV1")

        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS knowledge_base;")
        connection.commit()
        create_table_query = '''CREATE TABLE knowledge_base (
            term            text,
            sentences       text
        );'''
        cursor.execute(create_table_query)
        connection.commit()
        print('Table created successfully in PostgreSQL.')
        for term in facts.keys():
            facts[term] = [sentence.replace("'", "").replace("{", "").replace("}", "") for sentence in facts[term]]
            factsToInsert = '''[''' + '''{joinedFacts}'''.format(joinedFacts=''', '''.join(facts[term])) + ''']'''
            insert_query = '''INSERT INTO knowledge_base
                VALUES ('{term}',
                '{factsToInsert}');
            '''.format(term=term, factsToInsert=factsToInsert)
            cursor.execute(insert_query)
            connection.commit()
            print('Facts entered successfully to PostgreSQL')
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == '__main__':
    url = 'https://news.search.yahoo.com/search;_ylt=AwrFYnB2GA1kZ4crTCpXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMyNTQzNFNUXzEEc2VjA3BpdnM-?p=f1+news&fr2=piv-web&fr=news'
    print("Starting crawl...")
    URLSToScrape = BFSWebScraper(url)
    print("Finished crawl. Starting scrape...")
    scrapeURLS(URLSToScrape)
    print("Finished scrape. Starting clean...")
    clean()
    print("Finished clean. Starting extract...")
    mostCommonTokens = extract()
    print(mostCommonTokens)
    print("Finished extract. Starting to build knowledge base...")
    tokens = ['f1', 'hamilton', 'bull', 'mercedes', 'race', 'ferrari', 'champion', 'verstappen', 'prix', 'horner']
    facts = getFacts(tokens)
    createKB(facts)
    print("Finished creating knowledge base.")
