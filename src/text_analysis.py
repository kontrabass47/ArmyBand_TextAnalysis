#!/usr/bin/python3

import sys
import pandas as pd
from .vader_impl import Vader

class TextAnalysis:

    isFile = True

    def read(self):
        if (".xlsx" in sys.argv[0]) or (".csv" in sys.argv[0]):
            self.isFile = True

            file = sys.argv[0]
            column = input("Please enter the name of the column with text to parse: ")

            df_wp = pd.read_excel(file)
            df_wp.dropna()
            sentencelist = df_wp[column].tolist()

            vader = Vader()
            vader.analyzeFile(sentencelist)

        else:
            self.isFile = False


