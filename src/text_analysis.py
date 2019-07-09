#!/usr/bin/python3

import sys
import pandas as pd
from vader_impl import Vader
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from keyword_extraction import KeywordExtractor

class TextAnalysis:
    sentencelist = []

    def __init__(self):
        self.isFile = True

    def read(self):
        if (".xlsx" in sys.argv[1]) or (".csv" in sys.argv[1]):
            self.isFile = True

            file = '../docs/' + sys.argv[1]
            column = input("Please enter the name of the column with text to parse: ")

            df_wp = pd.read_excel(file)
            df_wp.dropna()

            sentencelist = df_wp[column].tolist()

            vader = Vader()
            vader.analyzeList(sentencelist)
            print('Vader Positive: {} Vader Negative: {}', vader.poscount, vader.negcount)
            print('Vader Polarity Average: ', vader.polarity)

            textblob = TextBlob()
            textblob.analyzeList(sentencelist)
            print('TextBlob Positive: {} TextBlob Negative: {}', textblob.poscount, textblob.negcount)
            print('TextBlob Polarity Average: ', textblob.polarity)

            naivebayes = NaiveBayes()
            naivebayes.analyzeList(sentencelist)
            print('NaiveBayes Positive: {} NaiveBayes Negative: {}', naivebayes.poscount, naivebayes.negcount)

        else:
            self.isFile = False


    def extractKeywords(self):
        extractor = KeywordExtractor()
        keywords = extractor.extractKeywords(self.sentencelist)
        print(keywords)

    # def normalize(self):


if __name__ == "__main__":
    textobj = TextAnalysis()
    textobj.read()
    textobj.extractKeywords()

