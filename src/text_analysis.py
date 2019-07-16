#!/usr/bin/python3

import sys
import pandas as pd
import xlsxwriter as excel
from datetime import datetime
from vader_impl import Vader
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from keyword_extraction import KeywordExtractor
from sentiment_analyzer import NormalizedObject
from result import Result
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



class TextAnalysis:

    def __init__(self):
        self.totalpos = 0
        self.totalneg = 0
        self.totalneu = 0
        self.avgConfidence = 0
        self.normalizedList = [] # contains list of normalized objects
        self.sentencelist = [] # contains list of sentences passed to program
        self.vader = Vader()
        self.textblob = TextBlob()
        self.naivebayes = NaiveBayes()

    def read(self, fileName):
        df_wp = None
        if ".xlsx" in fileName:
            df_wp = pd.read_excel(fileName)
        if ".csv" in fileName:
            df_wp = pd.read_csv(fileName)

        df_wp.dropna()

        self.sentencelist = df_wp["Text"].tolist()

        self.normalize(self.sentencelist)

        print("Total Positive: {} Total Negative: {} Total Neutral: {}"
                .format(self.totalpos, self.totalneg, self.totalneu))
        print("Average Confidence: {}%".format(round(self.avgConfidence * 100, 2)))


    def output(self):
        print("test")

    def countSentimentHelper(self, vader, textblob, naivebayes):
        numpos = 0
        numneg = 0
        numneu = 0
        if vader.classifier == "positive":
           numpos += 1
        if textblob.classifier == "positive":
            numpos += 1
        if naivebayes.classifier == "positive":
            numpos += 1
        if vader.classifier == "negative":
            numneg += 1
        if textblob.classifier == "negative":
            numneg += 1
        if naivebayes.classifier == "negative":
            numneg += 1
        if vader.classifier == "neutral":
            numneu += 1
        if textblob.classifier == "neutral":
            numneu += 1
        if naivebayes.classifier == "neutral":
            numneu += 1
        sentiments = {"pos" : numpos, "neg" : numneg, "neu" : numneu}
        return sentiments

    def normalize(self, sentencelist):
        self.vader.analyzeList(sentencelist)
        self.textblob.analyzeList(sentencelist)
        self.naivebayes.analyzeList(sentencelist)

        for i in range(0, len(self.vader.sentimentList)):
            nums = self.countSentimentHelper(
                    self.vader.sentimentList[i],
                    self.textblob.sentimentList[i],
                    self.naivebayes.sentimentList[i])
            normobj = NormalizedObject()

            # Calculate confidence level
            if nums['pos'] == 2 or nums['neg'] == 2 or nums['neu'] == 2:
                normobj.confidence = 1/3
            elif nums['pos'] == 3 or nums['neg'] == 3 or nums['neu'] == 3:
                normobj.confidence = 1
            else:
                normobj.confidence = 0

            # Calculate classifier
            if nums['pos'] > nums['neg'] and nums['pos'] > nums['neu']:
                self.totalpos += 1
                normobj.classifier = "positive"
            elif nums['neg'] > nums['pos'] and nums['neg'] > nums['neu']:
                self.totalneg += 1
                normobj.classifier = "negative"
            else:
                self.totalneu += 1
                normobj.classifier = "neutral"

            self.normalizedList.append(normobj)
            self.avgConfidence += normobj.confidence

        self.avgConfidence = self.avgConfidence / len(self.vader.sentimentList)

    # Creates and returns a Result object.
    def getResultObj(self, word, sentencelist):

        self.vader.analyzeList(sentencelist)
        self.textblob.analyzeList(sentencelist)
        self.naivebayes.analyzeList(sentencelist)

        numpos = 0
        numneg = 0
        numneu = 0
        total_confidence = 0;
        for i in range(0, len(self.vader.sentimentList)):
            nums = self.countSentimentHelper(
                    self.vader.sentimentList[i],
                    self.textblob.sentimentList[i],
                    self.naivebayes.sentimentList[i])
            numpos += nums['pos']
            numneg += nums['neg']
            numneu += nums['neu']

            confidence = 0
            # Calculate confidence level
            if nums['pos'] == 2 or nums['neg'] == 2 or nums['neu'] == 2:
                confidence = 1/3
            elif nums['pos'] == 3 or nums['neg'] == 3 or nums['neu'] == 3:
                confidence = 1
            else:
                confidence = 0

            total_confidence += confidence
        percentPositive = numpos / (numpos + numneg + numneu)
        avg_confidence = total_confidence / len(self.vader.sentimentList)
        result = Result(word, sentencelist, percentPositive, avg_confidence)
        return result

    # given pre-stemmed keywords:
    #   - loop through all sentences in data
    #   - add sentence to dictionary, where each keyword is mapped to list of sentences
    #     with that keyword
    #   - return that dictionary
    def getSentencesWithKeywords(self, stemmed_keywords, keyword_dict):
        stemmer = PorterStemmer()
        dictionary = {}
        for keyword in stemmed_keywords:                     # add all keywords to dict
            dictionary[keyword] = []
            keyword_dict[keyword] = 0
        for sentence in self.sentencelist:
            for keyword in stemmed_keywords:
                # if this keyword is in this sentence, add it to the list of sentences
                # associated with this keyword
                words = word_tokenize(sentence)
                stemmed_words = []                           # tokenize this sentence
                for word in words:                           # and stem all the words
                    stemmed_words.append(stemmer.stem(word)) # for easy comparison
                if keyword in stemmed_words:
                    # We only want to store the first 4 sentences or so
                    if len(dictionary[keyword]) < 4:
                        dictionary[keyword].append(sentence)
                    keyword_dict[keyword] += 1
        return dictionary

    def getResultsFromKeywordDictionary(self, dictionary):
        results = []
        for keyword in dictionary.keys():
            if dictionary[keyword]:
                result = self.getResultObj(keyword, dictionary[keyword])
                results.append(result)
        return results

    # creates the output file given a list of results. output is in the form of
    # an excel file
    def createOutputFile(self, results):
        words = []       # list of keywords
        sentences = []   # list of lists of sentences
        sentiments = []  # list of sentiments, represented as % positive
        confidences = [] # list of confidences, represented as % confidence
        for result in results:
            words.append(result.word)
            sentences.append(result.sentences)
            sentiments.append(result.sentiment)
            confidences.append(result.confidence)
        output = excel.Workbook('out.xlsx')
        sheet = output.add_worksheet()
        sheet.set_column(0, 0, 20)
        sheet.write(0, 0, 'Word/% Positive/% Confidence')
        sheet.write(0, 1, 'Sentences')
        rowCounter = 1
        for i in range(len(results)):
            sentiment_percent = '%.3f'%(results[i].sentiment * 100)
            confidence_percent = '%.3f'%(results[i].confidence * 100)
            sheet.write(rowCounter, 0, results[i].word)
            sheet.write(rowCounter + 1, 0, '{}% positive'.format(sentiment_percent))
            sheet.write(rowCounter + 2, 0, '{}% confident'.format(confidence_percent))
            for sentence in sentences[i]:
                sheet.write(rowCounter, 1, sentence)
                rowCounter += 1
            if len(sentences[i]) < 3:
                rowCounter += (3 - len(sentences[i]))
            rowCounter += 1
        output.close()

    # extracts keywords from the given list of sentences
    #   - if provided, custom stopwords will be used in extracting the keywords
    #   - if custom keywords are provided, this will return the prominence and 
    #     sentiment of sentences related to that keyword
    # note that there is NO guarantee that each sentence will be displayed only once.
    # sentences with more than one keyword can appear under multiple keywords
    def extractKeywords(self, keywords=None, stopwords=None):
        print("extracting keywords at {}".format(datetime.now().time()))
        extractor = KeywordExtractor()
        extracted_keywords = extractor.extractKeywords(self.sentencelist, keywords, stopwords)
        joined_keywords = " ".join(extracted_keywords)
        single_words = word_tokenize(joined_keywords)

        # if there are no keywords to look for, our work is done
        if keywords == None:
            return
        
        print("stemming keywords at {}".format(datetime.now().time()))

        # stemming all keywords for easier comparison
        stemmer =  PorterStemmer()
        stemmed_keywords = []
        for keyword in keywords:
            stemmed_word = stemmer.stem(keyword)
            stemmed_keywords.append(stemmed_word)

        # dictionary with keywords for keys, mapped to lists of sentences with
        # that keyword
        keyword_dict = {}
        print("getting sentences associated w/ keywords at {}".format(datetime.now().time()))
        dictionary = self.getSentencesWithKeywords(stemmed_keywords, keyword_dict)
        print("building printable results at {}".format(datetime.now().time()))
        results = self.getResultsFromKeywordDictionary(dictionary) 
        print("creating output file at {}".format(datetime.now().time()))
        self.createOutputFile(results)
        print("done extracting keywords at {}".format(datetime.now().time()))


if __name__ == "__main__":
    textobj = TextAnalysis()
    textobj.read()
    textobj.extractKeywords()

