from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from sentiment_analyzer import SentimentObject

# Sentiment analyzer using the Naive Bayes analyzer provided by Textblob,
# which is trained on movie reviews per their website.
class NaiveBayes(SentimentAnalyzer):

    # Constructor - initializes the analyzer and the sentiment list
    def __init__(self):
        self.analyzer = Blobber(analyzer=NaiveBayesAnalyzer())
        self.sentimentList = []

    # This analyzes a single string for sentiment. NOTICE that this method
    # asks that one passes in the naive bayes analyzer, since it's very
    # expensive to re-train it every time it's created.
    # Be sure to pass in Blobber(analyzer=NaiveBayesAnalyzer()), or else
    # it will create and train the analyzer each time, which takes up to 
    # 5 seconds.
    def analyzeString(self, text, analyzer=None):
        # Again, try to avoid this! It takes a LONG time!
        if analyzer is None:
            analyzer = Blobber(analyzer=NaiveBayesAnalyzer())
        sentiment = analyzer(text).sentiment
        obj = SentimentObject()
        if sentiment.classification == 'pos' and sentiment.p_pos > 0.51:
            obj.classifier = "positive"
        elif sentiment.classification == 'neg' and sentiment.p_neg > 0.51:
            obj.classifier = "negative"
        else:
            obj.classifier = "neutral"
        obj.sentence = text
        obj.aggregate = None # The naive bayes analyzer does not provide
                             # a compound score, unfortunately
        return obj

    # Analyzes a list of strings, using the analyzeString helper method.
    def analyzeList(self, sentence_list):
        # reset sentiment list before each iteration
        self.sentimentList = []
        for sentence in sentence_list:
            obj = self.analyzeString(sentence, self.analyzer)
            self.sentimentList.append(obj)
