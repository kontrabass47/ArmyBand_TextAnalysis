import pandas as pd
from tkinter import ttk, Tk, Frame, StringVar, Label, Button, Entry
from tkinter import LEFT, N, W, filedialog, messagebox
from tkinter.filedialog import askopenfilename
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from vader_impl import Vader
from text_analysis import TextAnalysis

fileUploadDefaultText = "Choose file"
optionalUploadDefaultText = "Choose a file (optional)"
defaultColumnName = "Text"

# Receives a file that has been uploaded. NOTHING is done until the submit
# button has been clicked
def uploadFile(event):
    file = askopenfilename()
    if file:
        uploadFileButtonText.set(file)

def uploadKeywords(event):
    file = askopenfilename()
    if file:
        uploadKeywordsButtonText.set(file)

def uploadStopwords(event):
    file = askopenfilename()
    if file:
        uploadStopwordsButtonText.set(file)

# Submits the selected file to be analyzed, and then displays the results
def submitFile(event):
    # file paths of provided file, and optionally keywords and stopwords
    fileName = uploadFileButtonText.get()
    keywordsName = uploadKeywordsButtonText.get()
    stopwordsName = uploadStopwordsButtonText.get()

    # prompt an alert if no file was selected, return
    if fileName == fileUploadDefaultText:
        messagebox.showinfo("Error", "No file selected")
        return
    
    # create lists of stopwords and keywords. lists are empty if not provided
    keywords = None
    stopwords = None
    if keywordsName != optionalUploadDefaultText:
        keywordFile = pd.read_excel(keywordsName)
        keywordFile.dropna()
        keywords = keywordFile[defaultColumnName].tolist()
    if stopwordsName != optionalUploadDefaultText:
        stopwordsFile = pd.read_excel(stopwordsName)
        stopwordsFile.dropna()
        stopwords = stopwordsFile[defaultColumnName].tolist()

    # analyze file and return results
    analyzer = TextAnalysis()
    analyzer.read(fileName)
    analyzer.extractKeywords(keywords, stopwords)
    uploadResultsString.set("check out the terminal for stuff")

# Receives a string, analyzes it, and displays the results
def submitText(event):
    vader = Vader()                             # sentiment analysis tools
    textblob = TextBlob()
    naivebayes = NaiveBayes()
    textInput = textEntry.get()                 # user-inputted string
    
    vaderObj = vader.analyzeString(textInput)   # results from each of the 
    tbObj = textblob.analyzeString(textInput)   # tools in the form of
    nbObj = naivebayes.analyzeString(textInput) # SentimentObject objects

    resultText = "Vader result: {}\n".format(vaderObj.classifier)
    resultText += "TextBlob result: {}\n".format(tbObj.classifier)
    resultText += "NaiveBayes result: {}\n".format(nbObj.classifier)
    textResultsString.set(resultText)

# Initialize all widgets in GUI here
root = Tk()
root.title("Sentiment Analysis Tool")

# Row 1 widgets: Text Label, Text Input, Text Submit
textLabel = Label(root, text="Enter Text")
textEntry = Entry(root, width=50)
textSubmitButton = Button(root, text="Submit")
textSubmitButton.bind("<Button-1>", submitText)

# Row 2 widgets: Text Analyzer Results Label
textResultsString = StringVar()
textResultsLabel = Label(root, anchor=N, textvariable=textResultsString, height=8)

# Row 3 widgets: File Label, File Upload, File Submit
uploadFileLabel = Label(root, text="Upload File")
uploadFileButtonText = StringVar()
uploadFileButtonText.set(fileUploadDefaultText)
uploadFileButton = Button(root, textvariable=uploadFileButtonText)
uploadFileButton.bind("<Button-1>", uploadFile)
fileSubmitButton = Button(root, text="Submit")
fileSubmitButton.bind("<Button-1>", submitFile)

# Row 4 widgets: Keywords Label, Keywords Upload, Keywords Submit
uploadKeywordsLabel = Label(root, text="Upload Keywords")
uploadKeywordsButtonText = StringVar()
uploadKeywordsButtonText.set(optionalUploadDefaultText)
uploadKeywordsButton = Button(root, textvariable=uploadKeywordsButtonText)
uploadKeywordsButton.bind("<Button-1>", uploadKeywords)

# Row 5 widgets: Stopwords Label, Stopwards Upload, Stopwards Submit
uploadStopwordsLabel = Label(root, text="Upload Stopwords")
uploadStopwordsButtonText = StringVar()
uploadStopwordsButtonText.set(optionalUploadDefaultText)
uploadStopwordsButton = Button(root, textvariable=uploadStopwordsButtonText)
uploadStopwordsButton.bind("<Button-1>", uploadStopwords)

# Row 6 widgets: File Analyzer Results Label
uploadResultsString = StringVar()
uploadResultsString.set("uploaded file results go here")
fileResultsLabel = Label(root, anchor=N, textvariable=uploadResultsString, height=15)



# All widgets are organized in a grid here
textLabel.grid(row=0, column=0, sticky=W)
textEntry.grid(row=0, column=1)
textSubmitButton.grid(row=0, column=2)

textResultsLabel.grid(row=1, column=1, sticky=W)

uploadFileLabel.grid(row=2, column=0, sticky=W)
uploadFileButton.grid(row=2, column=1, sticky=W)

uploadKeywordsLabel.grid(row=3, column=0, sticky=W)
uploadKeywordsButton.grid(row=3, column=1, sticky=W)

uploadStopwordsLabel.grid(row=4, column=0, sticky=W)
uploadStopwordsButton.grid(row=4, column=1, sticky=W)
fileSubmitButton.grid(row=4, column=2)

fileResultsLabel.grid(row=5, column=1, sticky=W)

root.mainloop()
