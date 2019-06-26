import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

# load in the dataframe
df = pd.read_csv("winemag-data-130k-v2.csv" , index_col=0)

# looking at first 5 rows of dataset
df.head()

#print("There are {} observations and {} features in this dataset. /n".format(df.shape[0],df.shape[1]))

country=df.groupby("country")

#plt.figure(figsize=(15,10))
#country.size().sort_values(ascending=False).plot.bar()
plt.xticks(rotation=50)
plt.xlabel("Country of Origin")
plt.ylabel("Number of Wines")
#plt.show()

#plt.figure(figsize=(15,10))
#country.max().sort_values(by="points", ascending=False)["points"].plot.bar()
plt.xticks(rotation=50)
plt.xlabel("Country of Origin")
plt.ylabel("Number of Wines")
#plt.show()


text = " ".join(review for review in df.description)
stopwords= set(STOPWORDS)
stopwords.update(["drink","now","wine","flavor","flavors"])
#wordcloud=WordCloud(stopwords=stopwords,background_color="white").generate(text)
#plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
           
           


# Save the image in the img folder:
#wordcloud.to_file("img/first_review.png")

