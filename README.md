# Sentiment Analysis of Army Band Feedback

This project aims to analyze feedback of the Army Band through the use of text collected via social media comments, surveys, and broadcasts.

## Technology Used
[TextBlob](https://textblob.readthedocs.io/en/dev/) and [Vader](https://github.com/cjhutto/vaderSentiment) are used to analyze the text.  
[rake-nltk](https://github.com/csurfer/rake-nltk) is used to extract key words from text.  
[Pandas](https://pandas.pydata.org/) is used to open and read the data files.  
[tkinter](https://docs.python.org/3/library/tkinter.html) is used to create the graphical UI  
[XlsxWriter](https://xlsxwriter.readthedocs.io/) is used to create and write to excel files  
[wordcloud](https://github.com/amueller/word_cloud) is used to create the wordcloud  
[seaborn](https://seaborn.pydata.org/#) is used for bar graphs and general data vis  
[tableau](https://www.tableau.com/) is used for other data vis stuff  

## Other references
None yet

## Getting Started
Make sure your Python version is 3.x or later.  
`pip install textblob vadersentiment pandas xlsxwriter` if your native Python is 3.x. Use `pip3` otherwise.  
`python3 view.py` can get you started with usage. See output.xlsx for your results.
