#!/usr/bin/python3

import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud,STOPWORDS
import string
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df_wp=pd.read_excel('../docs/ABIPerformanceFeedbackALL.xlsx')

df_wp=df_wp.rename(columns = {'Comments from Late Show Page':'Text'})
df_wp.dropna()

df_wplist=df_wp['Text'].tolist()
df_wpstr=str(df_wplist)

analyzer=SentimentIntensityAnalyzer()
for sentence in df_wplist:
    vs=analyzer.polarity_scores(sentence)
    scores=("{:-<65} {}".format(sentence, str(vs)))
    print(scores)
