#!/usr/bin/python3

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Vader:
    vaderSentimentList = [] # Contains as list of vaderSentiment objects

    def vaderAnalyzer(self):
        vader = Vader()
        print("All inputs are case sensitive!")
        file = input("Please enter the path to the .xlsx file to parse: ")
        column = input("Please enter the name of the column with text to parse: ")

        df_wp = pd.read_excel(file)
        df_wp.dropna()

        df_wplist = df_wp[column].tolist()

        analyzer = SentimentIntensityAnalyzer()

        counter = 0
        for sentence in df_wplist:
            vs = analyzer.polarity_scores(sentence)
            vader.sentimentList.append(vs)
            scores = ("Sentence {}: {}".format(counter, str(vs)))
            print(scores + " " )
            counter += 1

