from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

class NaiveBayes():

    def __init__(self):
        self.sentimentList = []
        self.negcount = 0
        self.poscount = 0
        self.polarity = 0

    def analyzeList(self, list):
        tb = Blobber(analyzer=NaiveBayesAnalyzer())
        print(tb("This is awful!!").sentiment.classification)
        for sentence in list:
            sentiment = tb(sentence).sentiment.classification
            if sentiment == 'neg':
                self.negcount += 1
            if sentiment == 'pos':
                self.poscount += 1

