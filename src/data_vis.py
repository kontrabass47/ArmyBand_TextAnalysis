# Used the follow datacamp for reference
# https://www.datacamp.com/community/tutorials/wordcloud-python

import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

def dataVis(fileName, stopwords):
    df = pd.read_excel(fileName)
    default_stopwords = set(STOPWORDS)
    if stopwords is not None:
        default_stopwords.update(stopwords)
    sentenceList = [str(sentence) for sentence in df["Text"].tolist()]
    sentences = " ".join(sentenceList)
    wordcloud = WordCloud(stopwords=default_stopwords, background_color="white")
    wordcloud.generate(sentences)

    wordcloud.to_file("../out/img.png")

    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis("off")
    #plt.show()
