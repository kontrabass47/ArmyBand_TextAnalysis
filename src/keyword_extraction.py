#!/usr/bin/python3
from rake_nltk import Metric, Rake

'''
This class takes in a list of strings, concatenates them into a single
paragraph, and then extracts key words/themes.
'''
class KeywordExtractor:

    def extractKeywords(self, sentences):
        rake = Rake(ranking_metric=Metric.WORD_FREQUENCY, max_length=3)
        text = " ".join(sentences)
        rake.extract_keywords_from_text(text)
        keywords = rake.get_ranked_phrases()
        print("keywords successfully extracted!")
        return keywords
