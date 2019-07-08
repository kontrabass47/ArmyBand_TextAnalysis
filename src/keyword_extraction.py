#!/usr/bin/python3
from rake_nltk import Rake

'''
This class takes in a list of strings, concatenates them into a single
paragraph, and then extracts key words/themes.
'''
class KeywordExtractor:
    __phrases = []

    def __init__(self, phrases):
        self.__phrases = phrases

    def extractKeywords(self):
        rake = Rake()
        keywords = rake.extract_keywords_from_sentences(self.__phrases)
        print("keywords successfully extracted!")
        return keywords
