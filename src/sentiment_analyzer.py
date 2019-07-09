
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