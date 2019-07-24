#!/usr/bin/python3

# Result is what is processed and printed on to the outputted excel file
# It contains:
#   - keyword
#   - snippets of sentences associated with that keyword
#   - % positivity of those snippets
#   - % confidence of that positivity rating
class Result:

    # constructor that initializes the object. no default values.
    def __init__(self, word, sentences, sentiment, confidence):
        self.word = word
        self.sentences = sentences
        self.sentiment = sentiment
        self.confidence = confidence

    # allows this object to be printed, for debugging purposes
    def __str__(self):
        return "Keyword: {}\n{}\nPercent Positive: {}\nConfidence: {}".format(
                self.word, self.sentences, self.sentiment, self.confidence)
