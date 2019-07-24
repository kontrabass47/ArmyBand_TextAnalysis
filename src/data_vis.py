import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# takes in a fileName and optional stopwords and creates a wordcloud
# fileName must be either a csv or xlsx file
# outputs a png image that the view displays in the UI

# Used the follow datacamp for reference
# https://www.datacamp.com/community/tutorials/wordcloud-python
def wordCloud(fileName, stopwords=None):
    df = None
    if ".xlsx" in fileName:
        df = pd.read_excel(fileName)
    elif ".csv" in fileName:
        df = pd.read_csv(fileName)
    default_stopwords = set(STOPWORDS)
    if stopwords is not None:
        default_stopwords.update(stopwords)
    sentenceList = [str(sentence) for sentence in df["Text"].tolist()]
    sentences = " ".join(sentenceList)
    wordcloud = WordCloud(stopwords=default_stopwords, background_color="white")
    wordcloud.generate(sentences)
    
    if not os.path.exists("../out/"):
        os.makedirs("../out/")
    wordcloud.to_file("../out/img.png")

# creates a simple bargaph of keywords on the x-axis and associated positivity
# value on the y-axis, from 0-100% positivity
# NOTE: currently does not work.

# used examples from seaborn docs here:
# https://seaborn.pydata.org/generated/seaborn.barplot.html
def barGraph(fileName):
    sns.set(style="whitegrid")
    df = None
    if ".xlsx" in fileName:
        df = pd.read_excel(fileName)
    elif ".csv" in fileName:
        df = pd.read_csv(fileName)
    ax = sns.barplot(x="Category", y="Sentences", data=df)
