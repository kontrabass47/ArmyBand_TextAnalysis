#!/usr/bin/python3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Vader():
    def __init__(self):
        self.sentimentList = [] # Contains as list of vaderSentiment objects (sentimentList[0]["neg"] accesses negative
        # element of first object



    def analyzeFile(self, list):
        print("All inputs are case sensitive!")

        analyzer = SentimentIntensityAnalyzer()

        counter = 0
        for sentence in list:
            vs = analyzer.polarity_scores(sentence)
            self.sentimentList.append(vs)
            counter += 1

