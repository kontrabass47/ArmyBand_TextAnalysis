# Used the follow datacamp for reference
# https://www.datacamp.com/community/tutorials/wordcloud-python

import numpy as np
import pandas as pd
import os
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


# takes in a fileName and optional stopwords and creates a wordcloud
# fileName must be either a csv or xlsx file
# outputs a png image that the view displays in the UI
def wordCloud(fileName, stopwords=None):
    df = pd.read_excel(fileName)
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
