
class SentimentAnalyzer():
    def __init__(self):
        self.sentimentList = []
        self.polarity = 0


class SentimentObject():
    def __init__(self):
        self.sentence = ""
        self.aggregate = 0
        self.classifier = ""


class NormalizedObject():
    def __init__(self):
        self.classifier = ""
        self.confidence = 0


    def __str__(self):
        return "Sentence: {} \nAggregate: {} \nClassifier: {}".format(self.sentence, self.aggregate, self.classifier)
