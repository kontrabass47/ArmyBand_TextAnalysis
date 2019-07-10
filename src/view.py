from tkinter import ttk, Tk, Frame, StringVar, Label, Button, Entry
from tkinter import LEFT, N, W, filedialog, messagebox
from tkinter.filedialog import askopenfilename
from textblob_impl import TextBlob
from naive_bayes_impl import NaiveBayes
from vader_impl import Vader

# Receives a file that has been uploaded. NOTHING is done until the submit
# button has been clicked
def uploadFile(event):
    file = askopenfilename()
    uploadFileButtonText.set(file)

# Submits the selected file to be analyzed, and then displays the results
def submitFile(event):
    fileName = uploadFileButtonText.get()
    if fileName == "Choose file":
        messagebox.showinfo("Error", "No file selected")
    else:
        uploadResultsString.set(fileName)


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

uploadResultsString = StringVar()
uploadFileButtonText = StringVar()
uploadResultsString.set("uploaded file results go here")
uploadFileButtonText.set("Choose file")
textResultsString = StringVar()
textLabel = Label(root, text="Enter Text")
uploadFileLabel = Label(root, text="Upload File")
textResultsLabel = Label(root, anchor=N, textvariable=textResultsString, height=8)
fileResultsLabel = Label(root, anchor=N, textvariable=uploadResultsString, height=15)
textEntry = Entry(root, width=50)
uploadFileButton = Button(root, textvariable=uploadFileButtonText)
uploadFileButton.bind("<Button-1>", uploadFile)
textSubmitButton = Button(root, text="Submit")
textSubmitButton.bind("<Button-1>", submitText)
fileSubmitButton = Button(root, text="Submit")
fileSubmitButton.bind("<Button-1>", submitFile)

# All widgets are organized in a grid here
textLabel.grid(row=0, column=0, sticky=W)
uploadFileLabel.grid(row=2, column=0, sticky=W)
textEntry.grid(row=0, column=1)
textResultsLabel.grid(row=1, column=1, sticky=W)
fileResultsLabel.grid(row=3, column=1, sticky=W)
uploadFileButton.grid(row=2, column=1, sticky=W)
textSubmitButton.grid(row=0, column=2)
fileSubmitButton.grid(row=2, column=2)

root.mainloop()
