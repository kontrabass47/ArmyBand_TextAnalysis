#!/usr/bin/python3
from rake_nltk import Metric, Rake
import nltk

'''
This class takes in a list of strings, concatenates them into a single
paragraph, and then extracts key words/themes.
'''
class KeywordExtractor:

    # extracts the first 30 key phrases, which are at most 7 words long,
    # and returns them. 30 are chosen because they are the most relevant
    def extractKeywords(self, sentences, user_keywords=None, user_stopwords=None):
        custom_stopwords = nltk.corpus.stopwords.words('english')
        more_words = ['band', 'performance', 'music', 'concert', 'brass', 
                'quintet']
        custom_punctuation = ['!!!', '!!', '...', '..']
        custom_stopwords.extend(more_words)
        custom_stopwords.extend(custom_punctuation)

        if user_stopwords != None:
            custom_stopwords.extend(user_stopwords)
        
        rake = Rake(
                ranking_metric=Metric.WORD_FREQUENCY, 
                stopwords=custom_stopwords,
                max_length=5)
        text = " ".join(sentences)
        rake.extract_keywords_from_text(text)
        keywords = rake.get_ranked_phrases()
        print("keywords successfully extracted!")
        return keywords[0:30]
