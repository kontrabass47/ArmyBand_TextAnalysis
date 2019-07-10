from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from sentiment_analyzer import SentimentObject

# Sentiment analyzer using the Naive Bayes analyzer provided by Textblob,
# which is trained on movie reviews per their website.
class NaiveBayes(SentimentAnalyzer):

    # This analyzes a single string for sentiment. NOTICE that this method
    # asks that one passes in the naive bayes analyzer, since it's very
    # expensive to re-train it every time it's created.
    # Be sure to pass in Blobber(analyzer=NaiveBayesAnalyzer()), or else
    # it will create and train the analyzer each time, which takes up to 
    # 5 seconds.
    def analyzeString(self, text, analyzer=None):
        # Again, try to avoid this! It takes a LONG time!
        if analyzer == None:
            analyzer = Blobber(analyzer=NaiveBayesAnalyzer())
        sentiment = analyzer(text).sentiment
        print("Naive Bayes Result")
        print(sentiment)
        obj = SentimentObject()
        if sentiment.classification == 'pos' and sentiment.p_pos > 0.51:
            self.poscount += 1
            obj.classifier = "positive"
        elif sentiment.classification == 'neg' and sentiment.p_neg > 0.51:
            self.negcount += 1
            obj.classifier = "negative"
        else:
            obj.classifier = "neutral"
        obj.sentence = text
        obj.aggregate = None # The naive bayes analyzer does not provide
                             # a compound score, unfortunately
        return obj

    # Analyzes a list of strings, using the analyzeString helper method.
    def analyzeList(self, list):
        tb = Blobber(analyzer=NaiveBayesAnalyzer())
        for sentence in list:
            obj = self.analyzeString(sentence, tb)
            self.sentimentList.append(obj)
