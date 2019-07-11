#!/usr/bin/python3

import sys
import pandas as pd
from vader_impl import Vader
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from keyword_extraction import KeywordExtractor
from sentiment_analyzer import NormalizedObject


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
        column = input("Please enter the name of the column with text to parse: ")
 
        df_wp = pd.read_excel(fileName)
        df_wp.dropna()

        self.sentencelist = df_wp[column].tolist()

        self.normalize(self.sentencelist)

       # self.avgConfidence = ((self.avgConfidence - (1/3)) / (1 - (1/3)))

        print("Total Positive: {} Total Negative: {} Total Neutral: {}".format(self.totalpos, self.totalneg, self.totalneu))
        print("Average Confidence: {}%".format(round(self.avgConfidence * 100, 2)))

        ''' Code Used for 
        
        vader = Vader()
        vader.analyzeList(self.sentencelist)
        print('Vader Positive: {} Vader Negative: {}'
                .format(vader.poscount, vader.negcount))
        print('Vader Polarity Average: ', vader.polarity)

        textblob = TextBlob()
        textblob.analyzeList(self.sentencelist)
        print('TextBlob Positive: {} TextBlob Negative: {}'
                .format(textblob.poscount, textblob.negcount))
        print('TextBlob Polarity Average: ', textblob.polarity)

        naivebayes = NaiveBayes()
        naivebayes.analyzeList(self.sentencelist)
        print('NaiveBayes Positive: {} NaiveBayes Negative: {}'
                .format(naivebayes.poscount, naivebayes.negcount))
        #print('Vader: ', vader.sentimentList[0])
        #print('TextBlob: ', textblob.sentimentList[0])
        #print('NaiveBayes: ', naivebayes.sentimentList[0])
        '''

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

            if numpos > numneg and numpos > numneu:
                self.totalpos += 1
                normobj.classifier = "positive"
                normobj.confidence = numpos / 3
            elif numneg > numpos and numneg > numneu:
                self.totalneg += 1
                normobj.classifier = "negative"
                normobj.confidence = numneg / 3
            elif numneu > numpos and numneu > numneg:
                self.totalneu += 1
                normobj.classifier = "neutral"
                normobj.confidence = numneu / 3
            else:
                normobj.classifier = "neutral"
                normobj.confidence = 0

            self.normalizedList.append(normobj)
            self.avgConfidence += normobj.confidence

        self.avgConfidence = self.avgConfidence / len(vader.sentimentList)


    def extractKeywords(self):
        extractor = KeywordExtractor()
        keywords = extractor.extractKeywords(self.sentencelist)
        print(keywords)

    # def normalize(self):


if __name__ == "__main__":
    textobj = TextAnalysis()
    textobj.read()
    textobj.extractKeywords()

