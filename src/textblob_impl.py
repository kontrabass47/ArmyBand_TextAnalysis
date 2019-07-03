#!/usr/bin/python3

import pandas as reader
from textblob import TextBlob

print("All inputs are case sensitive!")
file_name = input("Please enter the path to the .xlsx file to parse: ")
column_name = input("Please enter the name of the column with text to parse: ")

raw_excel_file = reader.read_excel(file_name)
raw_excel_file.dropna()

feedback_list = raw_excel_file[column_name].tolist()

counter = 0
for sentence in feedback_list:
    analyzer = TextBlob(sentence)
    scores=("Sentence {}: {}".format(counter, analyzer.sentiment))
    print(scores)
    counter += 1
