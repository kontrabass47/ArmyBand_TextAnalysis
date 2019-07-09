from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from sentiment_analyzer import SentimentObject

class NaiveBayes(SentimentAnalyzer):

    def analyzeList(self, list):
        tb = Blobber(analyzer=NaiveBayesAnalyzer())
        for sentence in list:
            sentiment = tb(sentence).sentiment
            if sentiment.classification == 'pos' and sentiment.p_pos > 0.51:
                self.poscount += 1
            if sentiment.classification == 'neg' and sentiment.p_neg > 0.51:
                self.negcount += 1

