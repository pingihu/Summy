# This is not our code. Credit: https://gist.github.com/igor-shevchenko/5821166
# coding: utf-8
# modified some thingzz -ping


from itertools import combinations
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from nltk import FreqDist
import nltk.data
import networkx as nx
import re
import json

def similarity(s1, s2):

    if not len(s1) or not len(s2):
        return 0.0
    elif not len(s1.intersection(s2)):
        return 0.0
    
    return len(s1.intersection(s2))/(1.3 * (len(s1) + len(s2)))

        
            

def textrank(text):
    sentences = sent_tokenize(text)
    
  
    
    tokenizer = RegexpTokenizer(r'\w+')
    lmtzr = EnglishStemmer()

    
    words = [set(lmtzr.stem(word) for word in tokenizer.tokenize(sentence))
                  for sentence in sentences]
    
    pairs = combinations(range(len(sentences)), 2)
    scores = [(i, j, similarity(words[i], words[j])) for i, j in pairs]
    scores = filter(lambda x: x[2], scores)
    
	
    g = nx.Graph()
    g.add_weighted_edges_from(scores)
    pr = nx.pagerank(g)
	
    return sorted(((i, pr[i], s) for i, s in enumerate(sentences) if i in pr), key=lambda x: pr[x[0]], reverse=True)



def extract(text, n):
    tr = textrank(text)
    top_n = sorted(tr[:n])
    return ' '.join(x[2] for x in top_n)

"""
The following loads test text froma  file
And formats it, stripping newline characters

"""
textToSumm = open("/Users/pingihu/Desktop/milgramexperiment.txt",'r')
textToSumm1 = open("/Users/pingihu/Desktop/milgramexperiment.txt",'r')
textToSumm2 = open("/Users/pingihu/Desktop/fucktosleep.txt",'r')
s = textToSumm.read().replace("\n", " ").replace("\r", " ")
s = re.sub(r'/[^a-zA-Z0-9\s\p{P}]/', "", s)


n = len(s.split('.'))
# summary is 1/4 the length of original text
n = int(round((n * .25)))

"""
the following removes questions automatically. this assumes we are summarizing
a textbook-- you wouldn't want questions in it

"""
txt = s.decode('utf-8')

summary = extract(txt,n)
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
summy_sentences_list_unclean = (sent_detector.tokenize(summary.strip()))
summy_sentences_list = []
for sentence in summy_sentences_list_unclean:
    summy_sentences_list.append(re.sub(r'.*\?$', " ", sentence))



"""
AND FINALLY,

The Summary of Ya Text
"""

print json.dumps(" ".join(summy_sentences_list))

