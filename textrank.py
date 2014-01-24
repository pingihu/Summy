# This is not our code. Credit: https://gist.github.com/igor-shevchenko/5821166
# coding: utf-8


from itertools import combinations
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
import networkx as nx

def similarity(s1, s2):
    if not len(s1) or not len(s2):
        return 0.0
    return len(s1.intersection(s2))/(1.0 * (len(s1) + len(s2)))

def textrank(text):
    sentences = sent_tokenize(text)
    tokenizer = RegexpTokenizer(r'\w+')
    lmtzr = RussianStemmer()
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

s = "The collapse of communism in the Soviet Union and Eastern Europe in the 1980s may be the most important change in the world during the past half century. Communist countries worked on the premise that government officials were in the best position to allocate the economy’s scarce resources. These central plan- ners decided what goods and services were produced, how much was produced, and who produced and consumed these goods and services. The theory behind central planning was that only the government could organize economic activity in a way that promoted economic well-being for the country as a whole. Most countries that once had centrally planned economies have abandoned the system and are instead developing market economies. In a market economy, the decisions of a central planner are replaced by the decisions of millions of firms and households. Firms decide whom to hire and what to make. Households decide which firms to work for and what to buy with their incomes. These firms Copyright 2011 Cengage Learning. All Rights Reserved. May not be copied, scanned, or duplicated, in whole or in part. Due to electronic rights, some third party content may be suppressed from the eBook and/or eChapter(s). Editorial review has deemed that any suppressed content does not materially affect the overall learning experience. Cengage Learning reserves the right to remove additional content at any time if subsequent rights restrictions require it. from the WAll street JournAl— PermIssIon, cArtoon feAtures sYndIcAte and households interact in the marketplace, where prices and self-interest guide their decisions. At first glance, the success of market economies is puzzling. In a market economy, no one is looking out for the economic well-being of society as a whole. Free markets contain many buyers and sellers of numerous goods and services, and all of them are interested primarily in their own well-being. Yet despite decentralized decision making and self-interested decision makers, market econo- mies have proven remarkably successful in organizing economic activity to pro- mote overall economic well-being. In his 1776 book An Inquiry into the Nature and Causes of the Wealth of Nations, economist Adam Smith made the most famous observation in all of econom- ics: Households and firms interacting in markets act as if they are guided by an “invisible hand” that leads them to desirable market outcomes. One of our goals in this book is to understand how this invisible hand works its magic. As you study economics, you will learn that prices are the instrument with which the invisible hand directs economic activity. In any market, buyers look at the price when determining how much to demand, and sellers look at the price when deciding how much to supply. As a result of the decisions that buyers and sellers make, market prices reflect both the value of a good to society and the cost to society of making the good. Smith’s great insight was that prices adjust to guide these individual buyers and sellers to reach outcomes that, in many cases, maximize the well-being of society as a whole. Smith’s insight has an important corollary: When the government prevents prices from adjusting naturally to supply and demand, it impedes the invisible hand’s ability to coordinate the decisions of the households and firms that make up the economy. This corollary explains why taxes adversely affect the alloca- tion of resources, for they distort prices and thus the decisions of households and firms. It also explains the great harm caused by policies that directly control prices, such as rent control. And it explains the failure of communism. In com- munist countries, prices were not determined in the marketplace but were dic- tated by central planners. These planners lacked the necessary information about consumers’ tastes and producers’ costs, which in a market economy is reflected in prices. Central planners failed because they tried to run the economy with one hand tied behind their backs—the invisible hand of the marketplace."

n = len(s.split('.'))
# summary is 1/4 the length of original text
n = int(round((n * .25)))
print extract(s.decode('utf-8'),n)
