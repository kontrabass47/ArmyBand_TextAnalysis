#!/usr/bin/python3


class Result:
    def __init__(self, word, sentences, sentiment, confidence):
        self.word = word
        self.sentences = sentences
        self.sentiment = sentiment
        self.confidence = confidence

    def __str__(self):
        return "Keyword: {}\n{}\nPercent Positive: {}\nConfidence: {}".format(
                self.word, self.sentences, self.sentiment, self.confidence)
