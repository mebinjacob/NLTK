'''
Created on 12-Feb-2013

@author: mebin
'''
from nltk import pos_tag, word_tokenize
from nltk.corpus import conll2007, gutenberg, ieer
from nltk.tag.stanford import NERTagger
import nltk
import re
from nltk.util import trigrams
mergedSpaceSeperatorConstant = '-';
locations = []
stanfordLocation = []
stanfordDate = []
#Chaining functions together
def ie_preprocess(document):
    s = nltk.sent_tokenize(document)
    s = [nltk.word_tokenize(sent) for sent in s]
    s = [nltk.pos_tag(sent) for sent in s]
    return s

# Named entity recognition
previousDateLoc = ''
def findNamedEntity():
    textFile = open('sentence.txt', 'r')
    sentence = ''
    previousDateLoc = 0
    for line in textFile:
#        print line
        stanfordNERExtractedLines = stanfordNERExtractor(line)
#        print stanfordNERExtractedLines
        for stanfordNERExtractedTuple in stanfordNERExtractedLines:
#            print stanfordNERExtractedTuple
#            for rel in nltk.sem.extract_rels('ORG', 'LOC', stanfordNERExtractedTuple, corpus='ieer', pattern = 'in'):
#                print rel
            if stanfordNERExtractedTuple[1] == 'LOCATION':
                stanfordLocation.append(stanfordNERExtractedTuple[0])
            if stanfordNERExtractedTuple[1] == 'DATE':
                if line.find(stanfordNERExtractedTuple[0]) == previousDateLoc:
                    stanfordDate.insert((len(stanfordDate) - 1), stanfordDate.pop(len(stanfordDate) - 1) + mergedSpaceSeperatorConstant +stanfordNERExtractedTuple[0])
                else:    
                    stanfordDate.append(stanfordNERExtractedTuple[0])
                previousDateLoc = line.find(stanfordNERExtractedTuple[0]) + len(stanfordNERExtractedTuple[0]) + 1
        sentence += line
    textFile.close()
    
    listPreprocessed = ie_preprocess(sentence)
    namedEntityList = []
    chunkedList = []
    for listPreprocess in listPreprocessed:
        chunkedList = nltk.ne_chunk(listPreprocess)
        class doc():
            pass
        doc.headline=['foo']
        doc.text=chunkedList
        IN = re.compile (r'in')#.*\bin\b(?!\b.+ing)
#        print 'before relation extraction', chunkedList
#        for rel in  nltk.sem.extract_rels('ORG','LOC',doc, corpus='ace', pattern=None):
#            print 'relation is', rel
        for i in range(0,len(chunkedList)):
            if type(chunkedList[i]) is nltk.tree.Tree:
                namedEntityList.insert(i, chunkedList[i])
    return namedEntityList

#Relation extraction
def relationExtractionForLocation():
    namedEntities = findNamedEntity()
    for namedEntity in namedEntities:
        print namedEntity 
        if namedEntity.node == 'GPE':
            if namedEntity.leaves()[0][1] == 'NNP':
                locations.append(namedEntity.leaves()[0][0])

def stanfordNERExtractor(sentence):
    st = NERTagger('english.muc.7class.distsim.crf.ser.gz', 'stanford-ner.jar')
    return st.tag(sentence.split()) 

relationExtractionForLocation()
fileToCommunicate = open('locationsDate.txt', 'w+')
print 'Tool 1'
fileToCommunicate.write('location: ')
newLocations = stanfordLocation + locations
for location in newLocations:
    fileToCommunicate.write(location )
    fileToCommunicate.write(",")

fileToCommunicate.write('\r\n')
fileToCommunicate.write('Date: ')
for date in stanfordDate:
    fileToCommunicate.write(date)
    fileToCommunicate.write(",")
fileToCommunicate.close()
print locations
print 'Tool 2' 
print  stanfordLocation
intersectedList = [val for val in locations if val in stanfordLocation]
print 'intersected list is'
print intersectedList
print 'The dates are '
print stanfordDate
