#sentiment analyses 4chan threads
from tkinter import *
from bs4 import BeautifulSoup
import basc_py4chan
from textblob import TextBlob
from time import sleep
from numpy import average

root = Tk()
frame = Frame(root,padx=10,pady=10)
frame.pack()
root.resizable(0,0)
root.wm_title("Sentiment Analysis of 4chan Threads")


def update():
	root.update()

def analyse(text):
	return text.sentiment.polarity

def analyseMean(textList):
	sentimentList=[]
	for entry in textList:
		sentimentList.append(entry[1].sentiment.polarity)
	return average(sentimentList)

def parse():
	text = textEntryContents.get()
	boards = boardEntryContents.get().split(",")
	posts = []
	if len(text) > 2  and len(boards) < 6:
		for b in boards:
			board = basc_py4chan.Board(b)
			threadList = board.get_all_threads()
			threadIter = 0
			for thread in threadList:
				if text.lower() in thread.topic.text_comment.lower():
					for post in thread.all_posts:
						postText = TextBlob(post.text_comment)
						print(postText)
						posts.append([board,postText,analyse(postText)])
						progressLabelContentsVerbose.set("Appended post #%s" % post.post_id)
						update()
				threadIter += 1
				progressLabelContents.set("Parsed thread %s out of %s in board /%s/" % (threadIter,len(threadList),b))
				sentimentLabelContents.set("Average polarity:")
				sentimentResultContents.set(str(analyseMean(posts)))
				update()
		progressLabelContents.set("Done")
		update()
	elif len(text) < 2 and len(boards) < 6:
		progressLabelContents.set("Longer text please!")
	elif len(text) > 2 and len(boards) > 6:
		progressLabelContents.set("Fewer boards please!\nPls don't kill the site's bandwidth!")
	elif len(text) < 2 and len(boards) > 6:
		progressLabelContents.set("What are you doing anon!\nFewer boards and longer text please!")


#User input and progress

boardsEntryLabel = Label(frame,text="Boards (separated by commas or spaces):",anchor="e")
boardsEntryLabel.grid(row=0,column=0)
boardEntryContents = StringVar()
boardsEntry = Entry(frame,textvariable=boardEntryContents)
boardsEntry.grid(row=0,column=1)

textEntryLabel = Label(frame,text="Text to analyse (>2 characters):",anchor="e")
textEntryLabel.grid(row=1,column=0)
textEntryContents = StringVar()
textEntry = Entry(frame,textvariable=textEntryContents)
textEntry.grid(row=1,column=1)

progressLabelContents = StringVar()
progressLabel = Label(frame,textvariable=progressLabelContents,width=34,height=2)
progressLabel.grid(row=2,column=1)

progressLabelContentsVerbose = StringVar()
progressLabel = Label(frame,textvariable=progressLabelContentsVerbose,width=34)
progressLabel.grid(row=3,column=1)

parseButton = Button(frame,text="Analyse",command=parse)
parseButton.grid(row=2,column=0)

#Analysis results

dataFrame = LabelFrame(frame,text="Results",height=400,width=200)
dataFrame.grid(columnspan=2,row=4)

sentimentLabelContents = StringVar()
sentimentLabelContents.set("No sentiment results yet")
sentimentLabel = Label(dataFrame,textvariable=sentimentLabelContents,width=34,height=2)
sentimentLabel.grid(row=0,column=0)

sentimentResultContents = StringVar()
sentimentResult = Label(dataFrame,textvariable=sentimentResultContents,width=34,height=2)
sentimentResult.grid(row=0,column=1)

mostPositivePostLabelContents = StringVar()
mostPositivePostLabel = Label(dataFrame,textvariable=sentimentLabelContents,width=34,height=2)

root.mainloop()
