#!/usr/bin/python3

import sys
import pandas as pd
from vader_impl import Vader
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from keyword_extraction import KeywordExtractor

class TextAnalysis:
    sentencelist = []

    def read(self, fileName=None):
        if fileName == None and (".xlsx" in sys.argv[1] or ".csv" in sys.argv[1]):
            fileName = '../docs/' + sys.argv[1]
        column = input("Please enter the name of the column with text to parse: ")
 
        df_wp = pd.read_excel(fileName)
        df_wp.dropna()

        sentencelist = df_wp[column].tolist()

        vader = Vader()
        vader.analyzeList(sentencelist)
        print('Vader Positive: {} Vader Negative: {}'
                .format(vader.poscount, vader.negcount))
        print('Vader Polarity Average: ', vader.polarity)

        textblob = TextBlob()
        textblob.analyzeList(sentencelist)
        print('TextBlob Positive: {} TextBlob Negative: {}'
                .format(textblob.poscount, textblob.negcount))
        print('TextBlob Polarity Average: ', textblob.polarity)

        naivebayes = NaiveBayes()
        naivebayes.analyzeList(sentencelist)
        print('NaiveBayes Positive: {} NaiveBayes Negative: {}'
                .format(naivebayes.poscount, naivebayes.negcount))
        #print('Vader: ', vader.sentimentList[0])
        #print('TextBlob: ', textblob.sentimentList[0])
        #print('NaiveBayes: ', naivebayes.sentimentList[0])

    def extractKeywords(self):
        extractor = KeywordExtractor()
        keywords = extractor.extractKeywords(self.sentencelist)
        print(keywords)

    # def normalize(self):


if __name__ == "__main__":
    textobj = TextAnalysis()
    textobj.read()
    textobj.extractKeywords()

