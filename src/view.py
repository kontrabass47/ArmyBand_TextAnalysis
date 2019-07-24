#!/usr/bin/python3

import pandas as pd
import tkinter as tk
import os
from tkinter import Tk, StringVar, Label, Button, Entry
from tkinter import N, W, messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from vader_impl import Vader
from text_analysis import TextAnalysis
from data_vis import wordCloud, barGraph

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


def submitFileWait(event):
    global win  # variable is global so it can be accessed in submitFile()
    win = tk.Tk()
    win.wm_title("Analyzer: ")

    label = tk.Label(win, text="Analyzing Data, Please Wait...")
    label.pack()
    win.after(200, submitFile)

# Submits the selected file to be analyzed, and then displays the results
def submitFile():
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

    resultText = "Total Positive: {}\n".format(analyzer.totalpos)
    resultText += "Total Negative: {}\n".format(analyzer.totalneg)
    resultText += "Total Neutral: {}\n".format(analyzer.totalneu)
    resultText += "Total Confidence: {}%".format(round(analyzer.avgConfidence * 100, 2))
    uploadResultsString.set(resultText)
    wordCloud(fileName, stopwords)
    img = ImageTk.PhotoImage(Image.open("../out/img.png"))
    wordCloudLabel.configure(image = img)
    wordCloudLabel.image = img
    os.remove("../out/img.png")    
   
    #barGraph("../out/out.xlsx")

    win.destroy()

    if keywordsName != optionalUploadDefaultText:
        winFinal = tk.Tk()
        winFinal.wm_title("Output: ")

        label = tk.Label(winFinal, text="Keyword file has been succesfully created!")
        label.pack()


# Receives a string, analyzes it, and displays the results
def submitText(event):
    vader = Vader()                             # sentiment analysis tools
    textblob = TextBlob()
    naivebayes = NaiveBayes()
    textobj = TextAnalysis()
    textInput = textEntry.get()                 # user-inputted string

    vaderObj = vader.analyzeString(textInput)   # results from each of the
    tbObj = textblob.analyzeString(textInput)   # tools in the form of
    nbObj = naivebayes.analyzeString(textInput) # SentimentObject objects

    arr = [textInput]
    textobj.normalize(arr)

    resultText = "Vader result: {}\n".format(vaderObj.classifier)
    resultText += "TextBlob result: {}\n".format(tbObj.classifier)
    resultText += "NaiveBayes result: {}\n".format(nbObj.classifier)
    resultText += "Final result: {}\n".format(textobj.normalizedList[0].classifier)
    resultText += "Confidence: {}%".format(round(textobj.normalizedList[0].confidence * 100, 2))
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
fileSubmitButton.bind("<Button-1>", submitFileWait)

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
fileResultsLabel = Label(root, anchor=N, textvariable=uploadResultsString, height=5)

# Row 7 widgets: Word Cloud Label
wordCloudLabel = Label(root)

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

wordCloudLabel.grid(row=6, column=1, sticky=W, pady=(0, 5))

if __name__ == "__main__":
    root.mainloop()
