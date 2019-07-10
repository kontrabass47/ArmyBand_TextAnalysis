from tkinter import ttk, Tk, Frame, StringVar, Label, Button, Entry, LEFT, N, W
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from vader_impl import Vader

# Functions that button presses will call from the GUI
def uploadFile(event):
    uploadResultsString.set("uploaded file results go here AHHH BUTTON")

def submitText(event):
    vader = Vader()
    textblob = TextBlob()
    naivebayes = NaiveBayes()

    textInput = textEntry.get()
    textList = [textInput]

    vader.analyzeList(textList)
    textblob.analyzeList(textList)
    naivebayes.analyzeList(textList)

    resultText = "Vader results:\n"
    resultText += "Positives: {}, Negatives: {}\n".format(vader.poscount, vader.negcount)
    resultText += "Polarity average: {}\n".format(vader.polarity)
    resultText += "TextBlob results:\n"
    resultText += "Positives: {}, Negatives: {}\n".format(textblob.poscount, textblob.negcount)
    resultText += "Polarity average: {}\n".format(textblob.polarity)
    resultText += "NaiveBayes results:\n"
    resultText += "Positives: {}, Negatives: {}\n".format(naivebayes.poscount, naivebayes.negcount)
    resultText += "Polarity average: {}\n".format(naivebayes.polarity)
    textResultsString.set(resultText)

# Initialize all widgets in GUI here
root = Tk()
root.title("Sentiment Analysis Tool")

uploadResultsString = StringVar()
uploadResultsString.set("uploaded file results go here")
textResultsString = StringVar()
textLabel = Label(root, text="Enter Text")
uploadFileLabel = Label(root, text="Upload File")
textResultsLabel = Label(root, anchor=N, textvariable=textResultsString, height=8)
fileResultsLabel = Label(root, anchor=N, textvariable=uploadResultsString, height=15)
textEntry = Entry(root, width=50)
uploadFileButton = Button(root, text="Choose file")
uploadFileButton.bind("<Button-1>", uploadFile)
textSubmitButton = Button(root, text="Submit")
textSubmitButton.bind("<Button-1>", submitText)

# All widgets are organized in a grid here
textLabel.grid(row=0, column=0, sticky=W)
uploadFileLabel.grid(row=2, column=0, sticky=W)
textEntry.grid(row=0, column=1)
textResultsLabel.grid(row=1, column=1, sticky=W)
fileResultsLabel.grid(row=3, column=1, sticky=W)
uploadFileButton.grid(row=2, column=1, sticky=W)
textSubmitButton.grid(row=0, column=2)

root.mainloop()
