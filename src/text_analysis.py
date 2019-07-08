#!/usr/bin/python3

import tkinter
import sys
import pandas as pd
from vader_impl import Vader

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
            print(vader.sentimentList[0]["neg"])

        else:
            self.isFile = False
            # process sentence


if __name__ == "__main__":
    textobj = TextAnalysis()
    textobj.read()
