from tkinter import ttk, Tk, Frame, StringVar, Label, Button, Entry, LEFT, N, W

# Functions that button presses will call from the GUI
def uploadFile(event):
    uploadResultsString.set("uploaded file results go here AHHH BUTTON")

def submitText(event):
    textInput = textEntry.get()
    textResultsString.set(textInput)

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
