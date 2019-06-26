import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud,STOPWORDS
import string
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df_wp=pd.read_excel('6-stringColbert.xlsx')

df_wp=df_wp.rename(columns = {'Comments from Late Show Page':'Comments'})
df_wp.dropna()

df_wplist=df_wp['Comments'].tolist()
df_wpstr=str(df_wplist)

df_keylist=['trust','understanding','builds trust','strengthens bonds','inspire','national values','national beliefs','preserves customs',
'culture','unites cultures','tells americas story','esprit de corps','supports community','community','mental health','emotional health','support',
'family','recruiting','resiliency','morale','quality','patriotism','proud','american','army','military','troops','soldier','service','duty','honor',
'professional']

#matches=[x for x in df_keylist if x in df_wpstr]

#print(Counter(matches))


stop_words= set(stopwords.words('english'))

comments_words=word_tokenize(df_wpstr)

comments_wordspunk=[x for x in comments_words if not re.fullmatch('[' + string.punctuation + ']', x)]

filtered_comments=[w for w in comments_wordspunk if not w in stop_words]
filtered_comments=[]

for w in comments_wordspunk:
    if w not in stop_words:
        filtered_comments.append(w)

#print(filtered_comments)

#filtered_commentstr=str(filtered_comments)

#print(Counter(filtered_comments).most_common(20))


#wordcloud=WordCloud(width=1200, height=800, margin=0).generate(filtered_commentstr)
#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")
#plt.margins(x=0,y=0)
#plt.show()


analyzer=SentimentIntensityAnalyzer()
for sentence in df_wplist:
    vs=analyzer.polarity_scores(sentence)
    scores=("{:-<65} {}".format(sentence, str(vs)))
    print(scores)
















                        

                        
























      


