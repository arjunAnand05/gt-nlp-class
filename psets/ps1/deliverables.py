import nltk,re
from nltk.tokenize import word_tokenize, sent_tokenize,RegexpTokenizer
from collections import defaultdict, Counter
from sets import Set

trainkey = 'train-imdb.bow'
devkey = 'dev-imdb.bow'
testkey = 'test-imdb.key'
tokenizer = RegexpTokenizer(r'\w+')
def populateDict(sentences, dict):
	for sentence in sentences:
		#words = nltk.word_tokenize(sentence)
		words = tokenizer.tokenize(sentence)
		for word in words:
			if re.search('[0-9]+',word):
				continue
			word  = word.lower()
			if word in dict:
				dict[word] += 1
			else:
				dict[word] = 1
		
	return dict
	
def printTokenTypeRatio(bowfile):
	wordTypes = Set([])
	singleWordTypes = Set([])
	tokenCount = 0
	with open(bowfile,'r') as keys:
		for keyline in keys:
			wordset = keyline.rstrip().split(' ')
			for wordcount in wordset:
				word,frequency = wordcount.split(':')
				wordTypes.add(word)
				tokenCount += int(frequency)
				if int(frequency) == 1 :
					singleWordTypes.add(word)
	print "For ",bowfile," Token count =",tokenCount," type count = ",len(wordTypes)," and single word count = ",len(singleWordTypes)
	return singleWordTypes

singleTrainWords = printTokenTypeRatio(trainkey)
singleDevWords = printTokenTypeRatio(devkey)
print "Common words = ",len(singleDevWords.difference(singleTrainWords))
				

