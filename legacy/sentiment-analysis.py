from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from decimal import *
from collections import Counter
from collections import OrderedDict
from string import digits
import csv
import re
import string
import pdb

def calculate_value(word_score):
    #create dictionary csv (with assigned values to words), average occurence of words and return total value 
    
    comment_val = []
    single_val = []
    freq_val = []
    dictionary = {}
    
    with open('dictionary.csv') as f:
        dict_reader = csv.reader(f)
        for row in dict_reader:
            dictionary[row[0]] = row[1]

    for word in word_score:
        if (word in dictionary):
            word_score[word][0] = float(dictionary[word])

    total_val = 0
    wordcount = 0
    for word in word_score:
        print("word: " + word)
        print(word_score[word])
        total_val += (word_score[word][0])*(word_score[word][1])
        wordcount += word_score[word][1]
    avg_val = (total_val/wordcount) * 10
    return (avg_val)


def split_string(my_list):
#inputs list of comments / splits the text / outputs frequency of all words
    
    word_list = []
    word_score = {}
    for comment in my_list:
        comment=comment.lower()
        comment = re.sub(r'[^\w\s]','',comment)
        
        single_word = comment.split ()
        word_list += single_word
    for word in word_list:
        if (len(word) >= 4) & (len(word) <= 12):
            if word in word_score:
                word_score[word] = [0, word_score[word][1] + 1]
            else:
                word_score[word] = [0,1]
    print(word_score) 
    return word_score

def get_comments():

    analyzer = SentimentIntensityAnalyzer()
    my_list = [] #list of comments

    with open ('master.csv' , newline='') as f: 
        reader = csv.reader(f) 

        for row in reader:
            vs = analyzer.polarity_scores(row[2])
            my_list += [row[2]]
    
    return my_list

if __name__ == '__main__':
  my_list = get_comments()
  #print(type(my_list))
  word_score = split_string(my_list)
  avg_val = calculate_value(word_score)
  print("Score is " + str(avg_val))
