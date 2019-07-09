#!/usr/bin/python3

from textblob import TextBlob as TextBlobAnalyzer
from sentiment_analyzer import SentimentAnalyzer
# This class uses the textblob library to performance sentiment analysis
# on a provided list of sentences.
class TextBlob(SentimentAnalyzer):

    # sentimentList - list of textblob sentiment analysis objects.
    # each object has access to sentiment.polarity and sentiment.subjectivity
    #   - polarity is a scale from -1.0 to 1.0, from negative to positive
    #   - subjectivity is a scale from 0.0 to 1.0, a measure of how opinionated
    #     the sentence is
    #def __init__(self):


    # analyzes the list of sentences passed in and populates the object's list
    # sentiment objects
    def analyzeList(self, list):
        counter = 0
        for sentence in list:
            analyzer = TextBlobAnalyzer(sentence)
            if analyzer.sentiment.polarity >= 0.001:
                self.poscount += 1
                counter += 1

            if analyzer.sentiment.polarity <= -0.001:
                self.negcount += 1
                counter += 1

            self.polarity += analyzer.sentiment.polarity
            self.sentimentList.append(analyzer.sentiment)
        self.polarity = self.polarity / counter
