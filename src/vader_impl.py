#!/usr/bin/python3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from sentiment_analyzer import SentimentObject

# This class uses the Vader library to perform sentiment analysis on text
class Vader(SentimentAnalyzer):

    # Analyzes a single string for sentiment. Used as a helper method
    # in AnalyzeList
    def analyzeString(self, text, analyzer=None):
        obj = SentimentObject()
        if (analyzer == None):
            analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(text)

        if vs['compound'] > 0.05:
            obj.classifier = "positive"
        elif vs['compound'] < -0.05:
            obj.classifier = "negative"
        else:
            obj.classifier = "neutral"
        obj.sentence = text
        obj.aggregate = vs['compound']
        return obj

    # Analyzes a list of string for sentiment, creating SentimentObjects relating
    # sentiment to each string
    def analyzeList(self, list):
        # reset its sentiment list and polarity every time this is called
        self.sentimentList = []
        self.polarity = 0
        counter = 0
        analyzer = SentimentIntensityAnalyzer()
        for sentence in list:
            obj = self.analyzeString(sentence, analyzer)
            self.polarity += obj.aggregate
            if (obj.classifier == "negative" or obj.classifier == "positive"):
                counter += 1
            self.sentimentList.append(obj)
        self.polarity = self.polarity / counter
