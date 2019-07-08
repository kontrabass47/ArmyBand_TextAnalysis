#!/usr/bin/python3

import sys
import pandas as pd
from vader_impl import Vader
from textblob_impl import TextBlob

class TextAnalysis:
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
            vader.analyzeFile(sentencelist)
            print(vader.sentimentList[1]["compound"])

            textblob = TextBlob()
            textblob.analyzeFile(sentencelist)
            print(textblob.sentimentList[1])

        else:
            self.isFile = False
            # process sentence

   # def normalize(self):



if __name__ == "__main__":
    textobj = TextAnalysis()
    textobj.read()
