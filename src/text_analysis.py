#!/usr/bin/python3

import sys
import pandas as pd
from vader_impl import Vader
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from keyword_extraction import KeywordExtractor
from sentiment_analyzer import NormalizedObject
from result import Result
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

class TextAnalysis:

    def __init__(self):
        self.totalpos = 0
        self.totalneg = 0
        self.totalneu = 0
        self.avgConfidence = 0
        self.normalizedList = [] # contains list of normalized objects
        self.sentencelist = [] # contains list of sentences passed to program

    def read(self, fileName=None):
        if fileName == None and (".xlsx" in sys.argv[1] or ".csv" in sys.argv[1]):
            fileName = '../docs/' + sys.argv[1]
 
        df_wp = pd.read_excel(fileName)
        df_wp.dropna()

        self.sentencelist = df_wp["Text"].tolist()

        self.normalize(self.sentencelist)

        print("Total Positive: {} Total Negative: {} Total Neutral: {}"
                .format(self.totalpos, self.totalneg, self.totalneu))
        print("Average Confidence: {}%".format(round(self.avgConfidence * 100, 2)))

    def normalize(self, sentencelist):
        vader = Vader()
        textblob = TextBlob()
        naivebayes = NaiveBayes()

        vader.analyzeList(sentencelist)
        textblob.analyzeList(sentencelist)
        naivebayes.analyzeList(sentencelist)

        for i in range(0, len(vader.sentimentList)):
            numpos = 0
            numneg = 0
            numneu = 0

            if vader.sentimentList[i].classifier == "positive":
                numpos += 1
            if textblob.sentimentList[i].classifier == "positive":
                numpos += 1
            if naivebayes.sentimentList[i].classifier == "positive":
                numpos += 1
            if vader.sentimentList[i].classifier == "negative":
                numneg += 1
            if textblob.sentimentList[i].classifier == "negative":
                numneg += 1
            if naivebayes.sentimentList[i].classifier == "negative":
                numneg += 1
            if vader.sentimentList[i].classifier == "neutral":
                numneu += 1
            if textblob.sentimentList[i].classifier == "neutral":
                numneu += 1
            if naivebayes.sentimentList[i].classifier == "neutral":
                numneu += 1

            normobj = NormalizedObject()

            # Calculate confidence level
            if numpos == 2 or numneg == 2 or numneu == 2:
                normobj.confidence = 1/3
            elif numpos == 3 or numneg == 3 or numneu == 3:
                normobj.confidence = 1
            else:
                normobj.confidence = 0

            # Calculate classifier
            if numpos > numneg and numpos > numneu:
                self.totalpos += 1
                normobj.classifier = "positive"
            elif numneg > numpos and numneg > numneu:
                self.totalneg += 1
                normobj.classifier = "negative"
            elif numneu > numpos and numneu > numneg:
                self.totalneu += 1
                normobj.classifier = "neutral"
            else:
                normobj.classifier = "neutral"

            self.normalizedList.append(normobj)
            self.avgConfidence += normobj.confidence

        self.avgConfidence = self.avgConfidence / len(vader.sentimentList)

    # given pre-stemmed keywords:
    #   - loop through all sentences in data
    #   - add sentence to dictionary, where each keyword is mapped to list of sentences
    #     with that keyword
    #   - return that dictionary
    def getSentencesWithKeywords(self, stemmed_keywords):
        stemmer = PorterStemmer()
        dictionary = {}
        for keyword in stemmed_keywords:                     # add all keywords to dict
            dictionary[keyword] = []
        for sentence in self.sentencelist:
            for keyword in stemmed_keywords:
                # if this keyword is in this sentence, add it to the list of sentences
                # associated with this keyword
                words = word_tokenize(sentence)
                stemmed_words = []                           # tokenize this sentence
                for word in words:                           # and stem all the words
                    stemmed_words.append(stemmer.stem(word)) # for easy comparison
                if keyword in stemmed_words:
                    dictionary[keyword].append(sentence)
        return dictionary

    def getResultsFromKeywordDictionary(self, dictionary):
        for keyword in dictionary.keys():
            # TODO:
            # analyze sentiment of associated list of sentences
            # build Result object with:
            #   - keyword
            #   - sentences
            #   - sentiment
            # HOW TO DO: refactor read to be more modular. take in sentences, spit out
            #            sentiment of those sentences
        return None

    # extracts keywords from the given list of sentences
    #   - if provided, custom stopwords will be used in extracting the keywords
    #   - if custom keywords are provided, this will return the prominence and 
    #     sentiment of sentences related to that keyword
    # note that there is NO guarantee that each sentence will be displayed only once.
    # sentences with more than one keyword can appear under multiple keywords
    def extractKeywords(self, keywords=None, stopwords=None):
        extractor = KeywordExtractor()
        extracted_keywords = extractor.extractKeywords(self.sentencelist, keywords, stopwords)
        print(extracted_keywords)
        joined_keywords = " ".join(extracted_keywords)
        single_words = word_tokenize(joined_keywords)

        # if there are no keywords to look for, our work is done
        if keywords == None:
            return
        
        # stemming all keywords for easier comparison
        stemmer = PorterStemmer()
        stemmed_keywords = []
        for keyword in keywords:
            stemmed_word = stemmer.stem(keyword)
            stemmed_keywords.append(stemmed_word)

        # dictionary with keywords for keys, mapped to lists of sentences with
        # that keyword
        dictionary = self.getSentencesWithKeywords(stemmed_keywords)
        results = self.getResultsFromKeywordDictionary(dictionary) 
        print(results)

        # stemming all words in the extracted keywords for easier comparison
        stemmed_words = []
        for word in single_words:
            stemmed_word = stemmer.stem(word)
            stemmed_words.append(stemmed_word)

        keyword_dict = {}
        # add all user-defined keywords to a dictionary, setting all counts to 0
        for keyword in stemmed_keywords:
            keyword_dict[keyword.lower()] = 0
        # go through the extracted keywords, counting instances of each
        # user-defined keyword as we go
        for word in single_words:
            stemmed_word = stemmer.stem(word)
            if stemmed_word in keyword_dict.keys():
                keyword_dict[stemmed_word] += 1
        print(keyword_dict)


if __name__ == "__main__":
    textobj = TextAnalysis()
    textobj.read()
    textobj.extractKeywords()

