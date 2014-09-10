import nltk,re
from nltk.tokenize import word_tokenize, sent_tokenize,RegexpTokenizer
from collections import defaultdict, Counter

trainkey = 'train-imdb.key'
devkey = 'dev-imdb-test.key'
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

def docsToBOWs(keyfile):
    with open(keyfile,'r') as keys:
        with open(keyfile.replace('.key','.bow'),'w') as outfile:
            for keyline in keys:
                dataloc = keyline.rstrip().split(' ')[0]
                fcounts = dict([])
                with open(dataloc,'r') as infile:
                    for line in infile:
						populateDict(sent_tokenize(line), fcounts)
                for word,count in fcounts.items():
                    print >>outfile,"{}:{}".format(word,count), #write the word and its count to a line
                print >>outfile,""
				
offset = '**OFFSET**'
def dataIterator(keyfile):
    with open(keyfile.replace('key','bow'),'r') as bows:
        with open(keyfile,'r') as keys:
            for keyline in keys:
                textloc,label = keyline.rstrip().split(' ')
                fcounts = {word:int(count) for word,count in\
                           [x.split(':') for x in bows.readline().rstrip().split(' ')]}
                fcounts[offset] = 1
                yield fcounts,label


def getAllCounts(datait):
    allcounts = Counter()
    for fcounts, _ in datait:
        allcounts += Counter(fcounts)
    return allcounts

	
#docsToBOWs(trainkey)
ac_train = getAllCounts(dataIterator('train-imdb.key'))
#ac_dev = getAllCounts(dataIterator('dev-imdb.key'))
#ac_test = getAllCounts(dataIterator('test-imdb.key'))
print "number of word types",len(ac_train.keys())-1
print "most common",ac_train.most_common(20)
