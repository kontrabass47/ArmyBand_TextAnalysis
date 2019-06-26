import pandas as pd
import csv
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud,STOPWORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df_holiday=pd.read_csv('HolidayShow2018Comments_Time.csv', encoding='ISO-8859-1')

comments=df_holiday['Comment'].astype('object')


#stopwords= set(STOPWORDS)

#wordcloud= WordCloud(stopwords=stopwords,background_color='white').generate_most_common(comments)

#plt.imshow(wordcloud,interpolation='bilinear')
#plt.axis("off")
#plt.show()

#comments.str.split(expand=True)

analyzer=SentimentIntensityAnalyzer()
for sentence in comments:
    vs=analyzer.polarity_scores(sentence)
    scores=("{:-<65} {}".format(sentence, str(vs)))
    print(scores)



        



        
    
    

        
        
            
            
    
    





           












    




