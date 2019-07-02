import pandas as pd
import csv
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud,STOPWORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

comments=pd.read_csv('OpenText1.csv')

text=comments['Comment']


most_common=" ".join(review for review in comments.Comment)
stopwords= set(STOPWORDS)

wordcloud= WordCloud(stopwords=stopwords,background_color='white').generate(most_common)

plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
plt.show()



#comments.Comment.str.split(expand=True)

#analyzer=SentimentIntensityAnalyzer()
#for sentence in text:
    #vs=analyzer.polarity_scores(sentence)
    #scores=("{:-<65} {}".format(sentence, str(vs)))
    #print(scores)
