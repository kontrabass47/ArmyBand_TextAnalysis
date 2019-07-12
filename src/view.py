from tkinter import ttk, Tk, Frame, StringVar, Label, Button, Entry
from tkinter import LEFT, N, W, filedialog, messagebox
from tkinter.filedialog import askopenfilename
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from vader_impl import Vader
from text_analysis import TextAnalysis

# Receives a file that has been uploaded. NOTHING is done until the submit
# button has been clicked
def uploadFile(event):
    file = askopenfilename()
    uploadFileButtonText.set(file)

def uploadKeywords(event):
    file = askopenfilename()
    uploadKeywordsButtonText.set(file)

def uploadStopwords(event):
    file = askopenfilename()
    uploadStopwordsButtonText.set(file)

# Submits the selected file to be analyzed, and then displays the results
def submitFile(event):
    fileName = uploadFileButtonText.get()
    if fileName == "Choose file":
        messagebox.showinfo("Error", "No file selected")
    else:
        analyzer = TextAnalysis()
        analyzer.read(fileName)
        uploadResultsString.set("check out the terminal for stuff")

def submitKeywords(event):
    fileName = uploadKeywordsButtonText.get()

def submitStopwords(event):
    fileName = uploadStopwordsButtonText.get()

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
uploadFileButtonText.set("Choose file")
uploadFileButton = Button(root, textvariable=uploadFileButtonText)
uploadFileButton.bind("<Button-1>", uploadFile)
fileSubmitButton = Button(root, text="Submit")
fileSubmitButton.bind("<Button-1>", submitFile)

# Row 4 widgets: Keywords Label, Keywords Upload, Keywords Submit
uploadKeywordsLabel = Label(root, text="Upload Keywords")
uploadKeywordsButtonText = StringVar()
uploadKeywordsButtonText.set("Choose file")
uploadKeywordsButton = Button(root, textvariable=uploadKeywordsButtonText)
uploadKeywordsButton.bind("<Button-1>", uploadKeywords)
keywordsSubmitButton = Button(root, text="Submit")
keywordsSubmitButton.bind("<Button-1>", submitKeywords)

# Row 5 widgets: Stopwords Label, Stopwards Upload, Stopwards Submit
uploadStopwordsLabel = Label(root, text="Upload Stopwords")
uploadStopwordsButtonText = StringVar()
uploadStopwordsButtonText.set("Choose file")
uploadStopwordsButton = Button(root, textvariable=uploadStopwordsButtonText)
uploadStopwordsButton.bind("<Button-1>", uploadStopwords)
stopwordsSubmitButton = Button(root, text="Submit")
stopwordsSubmitButton.bind("<Button-1>", submitStopwords)

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
fileSubmitButton.grid(row=2, column=2)

uploadKeywordsLabel.grid(row=3, column=0, sticky=W)
uploadKeywordsButton.grid(row=3, column=1, sticky=W)
keywordsSubmitButton.grid(row=3, column=2)

uploadStopwordsLabel.grid(row=4, column=0, sticky=W)
uploadStopwordsButton.grid(row=4, column=1, sticky=W)
stopwordsSubmitButton.grid(row=4, column=2)

fileResultsLabel.grid(row=5, column=1, sticky=W)

root.mainloop()
