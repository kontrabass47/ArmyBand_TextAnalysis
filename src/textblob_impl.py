#!/usr/bin/python3

import pandas as reader
from textblob import TextBlob

# Excel files must be formatted as such:
# If there are 5 ratings, they must be from 0-4, ordered worst to best

# User will type in relative path of the excel file and column names of text and ratings
print("All inputs are case sensitive!")
file_name = input("Please enter the path to the .xlsx file to parse: ")
column_name = input("Please enter the name of the column with text to parse: ")
rating_column = input("Please enter the name of the column with numerical ratings: ")

# pandas opens the excel file and removes all erroneous entries
raw_excel_file = reader.read_excel(file_name)
raw_excel_file.dropna()

# this converts the columns containing the text and the ratings to lists for accessibility
feedback_list = raw_excel_file[column_name].tolist()
rating_list = raw_excel_file[rating_column].tolist()

# to measure accuracy, we first count how many actual pieces of feedback belong in each
# category
actual_very_dissatisfied = 0
actual_dissatisfied = 0
actual_neutral = 0
actual_satisfied = 0
actual_very_satisfied = 0
'''
for rating in rating_list:
    if rating == 0:
        actual_very_dissatisfied += 1
    elif rating == 1:
        actual_dissatisfied += 1
    elif rating == 2:
        actual_neutral += 1
    elif rating == 3:
        actual_satisfied += 1
    elif rating == 4:
        actual_very_satisfied += 1
'''
# this will classify each sentence with the TextBlob model, and will report TextBlob's
# accuracy once it is finished.
counter = 0
reported_very_dissatisfied = 0
reported_dissatisfied = 0
reported_neutral = 0
reported_satisfied = 0
reported_very_satisfied = 0

for sentence in feedback_list:
    analyzer = TextBlob(sentence)
    scores = ("Sentence {}: {}".format(counter, analyzer.sentiment))
    polarity = analyzer.sentiment.polarity

    
    rating = rating_list[counter]
    if rating == 0:
        if polarity < -0.5:
            reported_very_dissatisfied += 1
        actual_very_dissatisfied += 1
    elif rating == 1:
        if polarity >= -0.5 and polarity < 0.1:
            reported_dissatisfied += 1
        actual_dissatisfied += 1
    elif rating == 2:
        if polarity >= -0.1 and polarity < 0.25:
            reported_neutral += 1
        actual_neutral += 1
    elif rating == 3:
        if polarity >= 0.25 and polarity < 0.5:
            reported_satisfied += 1
        actual_satisfied += 1
    elif rating == 4:
        if polarity >= 0.5:
            reported_very_satisfied += 1
        actual_very_satisfied += 1

    print(scores)
    counter += 1

# print out how accurate it is. hopefully it is not garbage.
print(reported_very_dissatisfied / actual_very_dissatisfied)
print(reported_dissatisfied / actual_dissatisfied)
print(reported_neutral / actual_neutral)
print(reported_satisfied / actual_satisfied)
print(reported_very_satisfied / actual_very_satisfied)
