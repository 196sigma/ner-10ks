import re
import pprint
import nltk
from bs4 import BeautifulSoup

def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

## Remove HTML tables and tags
soup = BeautifulSoup(open('goog-10k-2016.html','r'), "lxml")
for table_tag in soup.findAll('table'):
    table_tag.extract()

#doc = [line.decode('utf-8').strip() for line in open('goog-item1-2016.txt','r')]
#doc = ' '.join(doc)
doc = soup.text
doc = str(doc.encode('ascii', 'ignore'))

sents = ie_preprocess(doc)

#nechunk = nltk.ne_chunk(sents[0])
nechunk = nltk.ne_chunk_sents(sents)

entity_names = []
for n in nechunk:
    for s in n.subtrees():
        if s.label() in ['ORGANIZATION']:
            entity_names.append(s.leaves().pop()[0])
en_dict = {} 
for x in entity_names:
    if x in en_dict:
            en_dict[x] += 1
    else:
            en_dict[x] = 1

#for x in en_dict:
#    print x, en_dict[x]
