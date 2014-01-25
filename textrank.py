# This is not our code. Credit: https://gist.github.com/igor-shevchenko/5821166
# coding: utf-8
# modified some thingzz -ping


from itertools import combinations
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
from nltk.stem.snowball import EnglishStemmer
import nltk.data
import networkx as nx
import re

def similarity(s1, s2):

    if not len(s1) or not len(s2):
        return 0.0
    elif not len(s1.intersection(s2)):
        return 0.0
    #return len(s1.intersection(s2))/(1.0 * (len(s1) + len(s2)))
    return len(s1.intersection(s2))/(2.0 * (len(s1) + len(s2)))

def textrank(text):
    sentences = sent_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    #lmtzr = RussianStemmer()
    lmtzr = EnglishStemmer()
    words = [set(lmtzr.stem(word) for word in tokenizer.tokenize(sentence.lower()))
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

textToSumm = open("/Users/pingihu/Desktop/milgramexperiment.txt",'r')
s = textToSumm.read().strip("\n")
#the following removes questions automatically. this assumes we are summarizing
#a textbook-- you wouldn't want questions in it
s = re.sub(r'\..*[a-zA-Z0-9]*\?$', ".", s)
n = len(s.split('.'))
# summary is 1/4 the length of original text
n = int(round((n * .25)))
summary = extract(s.decode('utf-8'),n)
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
summy_sentences_list_unclean = (sent_detector.tokenize(summary.strip()))
summy_sentences_list = []
for sentence in summy_sentences_list_unclean:
    summy_sentences_list.append(re.sub(r'.*\?$', " ", sentence))
#ummary = re.sub(r'[\? ||\. ][a-zA-Z0-9]*\?$', '', summary)
print " ".join(summy_sentences_list)

