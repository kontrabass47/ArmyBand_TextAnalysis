#!/usr/bin/python3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentiment import Sentiment

class Vader(Sentiment):

    def analyzeList(self, list):
        print("All inputs are case sensitive!")

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
            counter += 1
        self.polarity = self.polarity / counter
