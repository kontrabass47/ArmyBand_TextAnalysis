
class SentimentAnalyzer():
    def __init__(self):
        self.sentimentList = []
        self.negcount = 0
        self.poscount = 0
        self.polarity = 0


class SentimentObject():
    def __init__(self):
        self.sentence = ""
        self.aggregate = 0
        self.classifier = ""

    def __str__(self):
        return "Sentence: {} \nAggregate: {} \nClassifier: {}".format(self.sentence, self.aggregate, self.classifier)
