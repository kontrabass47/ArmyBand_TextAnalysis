#!/usr/bin/python3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from sentiment_analyzer import SentimentObject

class Vader(SentimentAnalyzer):

    def analyzeList(self, list):

        analyzer = SentimentIntensityAnalyzer()

        counter = 0
        for sentence in list:
            vs = analyzer.polarity_scores(sentence)
            if not vs['neg'] > 0.05:
                self.poscount += 1
                counter += 1
            if not vs['pos'] > 0.05:
                self.negcount += 1
                counter += 1
            self.polarity += vs['compound']
            self.sentimentList.append(vs)
        self.polarity = self.polarity / counter
