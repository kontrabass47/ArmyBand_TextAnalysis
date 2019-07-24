#!/usr/bin/python3

import pandas as pd
import xlsxwriter as excel
import os
from vader_impl import Vader
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from keyword_extraction import KeywordExtractor
from sentiment_analyzer import NormalizedObject
from result import Result
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer


# This class is responsible for all things analyzing. It opens and reads files,
# performs sentiment analysis, and creates the output file.
class TextAnalysis:

    # Constructor
    #   - totalpos is the total number of positive sentences in the file
    #   - totalneg is the total number of negative sentences in the file
    #   - totalneu is the total number of neutral sentences in the file
    #   - avgConfidence is the program's confidence in classifying the entire file
    #   - normalizedList is each sentence's associated classifier/confidence
    #   - sentenceList is the list of sentences to be analyzed from the file
    #   - vader, textblob, naivebayes are all analyzers
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

    # opens and reads a given file with data, analyzes it, and outputs the results
    #   - fileName is the name of the file. must be either excel or csv file
    def read(self, fileName):
        df_wp = None
        if ".xlsx" in fileName:
            df_wp = pd.read_excel(fileName)
        if ".csv" in fileName:
            df_wp = pd.read_csv(fileName)
        df_wp.dropna()
        self.sentencelist = [str(sentence) for sentence in df_wp["Text"].tolist()] 
        self.normalize(self.sentencelist)
        print("Total Positive: {} Total Negative: {} Total Neutral: {}"
                .format(self.totalpos, self.totalneg, self.totalneu))
        print("Average Confidence: {}%".format(round(self.avgConfidence * 100, 2)))

    # helper method for self.noramlize and self.getResultObj
    # takes in the results from the vader, textblob, and naivebayes analyzers
    # and determines the total number of positive, neutral, and negative ratings
    # from all of the analyzers combined
    # NOTE: once more analyzers are implemented, this method should take in a list
    # of analyzed objects rather than individual ones
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

    # Analyzes a list of sentences and mutates this object's counters for total
    # positive, neutral, and negative sentences. Additionally, it calculates and
    # mutates the value for the average confidence for all given sentences
    # This method also updates self.normalizedList to contain associated info
    # for sentences in self.sentencelist
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

    # Creates and returns a Result object. Does a similar thing to self.normalize
    # but it does not mutate this object's member variables
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

    # returns a substring of a sentence around a given index.
    #   - sentence_tokens is a whitespace-delimited list of words in a sentence
    #   - index is the index of the keyword in that split sentence
    def getContextOfSubstring(self, sentence_tokens, index):
        leftLimit = (index - 15, 0)[index - 15 < 0]
        rightLimit = (index + 15, len(sentence_tokens) - 1)[index + 15 >= len(sentence_tokens)]
        context_tokens = sentence_tokens[leftLimit : rightLimit]
        return TreebankWordDetokenizer().detokenize(context_tokens)

    # given pre-stemmed keywords:
    #   - loop through all sentences in data
    #   - add sentence to dictionary, where each keyword is mapped to list of sentences
    #     with that keyword
    #   - return that dictionary
    def getSentencesWithKeywords(self, stemmed_keywords, keyword_dict):
        stemmer = PorterStemmer()
        dictionary = {}
        for keyword in stemmed_keywords:                     # add all keywords to dict
            dictionary[keyword] = set()
            keyword_dict[keyword] = 0
        for sentence in self.sentencelist:
            stemmed_tokens = list(map(stemmer.stem, word_tokenize(sentence)))
            for keyword in stemmed_keywords:
                # if this keyword is in this sentence, add it to the list of sentences
                # associated with this keyword
                for word in stemmed_tokens:
                    if keyword == word:
                        tokens = word_tokenize(sentence)
                        stemmed_tokens = list(map(stemmer.stem, tokens))
                        context = self.getContextOfSubstring(tokens, 
                                stemmed_tokens.index(keyword))
                        dictionary[keyword].add(context)
                        keyword_dict[keyword] += 1
                        continue
        return dictionary

    # Loops through the given dictionary of keyword to sentences with that keyword
    # and returns a list of Result objects that can be outputted to an excel file.
    # Refer to self.getResultObj and result.py for details on the Result object.
    def getResultsFromKeywordDictionary(self, dictionary):
        results = []
        for keyword in dictionary.keys():
            if len(dictionary[keyword]) > 0:
                result = self.getResultObj(keyword, dictionary[keyword])
                results.append(result)
        return results

    # creates the output file given a list of results. output is in the form of
    # an excel file called out.xlsx in the out/ directory.
    # each keyword will only have the first 5 associated sentences printed
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
        if not os.path.exists("../out/"):
            os.makedirs("../out/")
        output = excel.Workbook('../out/out.xlsx')
        sheet = output.add_worksheet()
        sheet.set_column(0, 0, 20)
        sheet.write(0, 0, 'Category')
        sheet.write(0, 1, 'Sentences')
        rowCounter = 1
        for i in range(len(results)):
            sentiment_percent = '%.1f'%(results[i].sentiment * 100)
            confidence_percent = '%.1f'%(results[i].confidence * 100)
            sheet.write(rowCounter, 0, results[i].word)
            sheet.write(rowCounter + 1, 0, '{}% positive'.format(sentiment_percent))
            sheet.write(rowCounter + 2, 0, '{}% confident'.format(confidence_percent))
            written = 0 
            for sentence in sentences[i]:
                sheet.write(rowCounter, 1, sentence)
                rowCounter += 1
                written += 1
                if written > 5:
                    break
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
        extractor = KeywordExtractor()
        extracted_keywords = extractor.extractKeywords(self.sentencelist, stopwords)
        joined_keywords = " ".join(extracted_keywords)
        single_words = word_tokenize(joined_keywords)

        # if there are no keywords to look for, our work is done
        if keywords is None:
            return

        # stemming all keywords for easier comparison

        stemmer = PorterStemmer()
        stemmed_keywords = set()
        for keyword in keywords:
            stemmed_word = stemmer.stem(keyword)
            stemmed_keywords.add(stemmed_word)

        # dictionary with keywords for keys, mapped to lists of sentences with
        # that keyword
        keyword_dict = {}
        dictionary = self.getSentencesWithKeywords(stemmed_keywords, keyword_dict)
        results = self.getResultsFromKeywordDictionary(dictionary) 
        self.createOutputFile(results)
