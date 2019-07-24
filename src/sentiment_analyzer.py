# Parent of all impl classes (Vader, Textblob, naive_bayes)
class SentimentAnalyzer:
    def __init__(self):
        self.sentimentList = []  # List of sentiment objects
        self.polarity = 0  # L

# Sentiment object used by each impl class, not normalized
class SentimentObject:
    def __init__(self):
        self.sentence = ""
        self.aggregate = 0  # Decimal score depending on algorithm
        self.classifier = ""

    def __str__(self):
        return "Sentence: {} \nAggregate: {} \nClassifier: {}".format(self.sentence, self.aggregate, self.classifier)

# Takes SentimentObjects and combines them into one score (Each sentence in sentenceList gets evaluated once by each
# algorithm, for a total of 3 SentimentObjects for one sentence. This takes those 3 and normalizes them into one object
class NormalizedObject:
    def __init__(self):
        self.classifier = ""
        self.confidence = 0

