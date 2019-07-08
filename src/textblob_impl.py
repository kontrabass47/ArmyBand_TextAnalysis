#!/usr/bin/python3

from textblob import TextBlob

# This class uses the textblob library to performance sentiment analysis
# on a provided list of sentences.
class TextBlob():

    # sentimentList - list of textblob sentiment analysis objects.
    # each object has access to sentiment.polarity and sentiment.subjectivity
    #   - polarity is a scale from -1.0 to 1.0, from negative to positive
    #   - subjectivity is a scale from 0.0 to 1.0, a measure of how opinionated
    #     the sentence is
    def __init__(self):
        self.sentimentList = []

    # analyzes the list of sentences passed in and populates the object's list
    # sentiment objects
    def analyzeFile(self, list):
        print("All inputs are case sensitive!")
        counter = 0
        for sentence in feedback_list:
            analyzer = TextBlob(sentence)
            self.sentimentList.append(analyzer)
            scores = ("Sentence {}: {}".format(counter, analyzer.sentiment))
            print(scores)
            counter += 1
