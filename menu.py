# MARIO PORTILLO HERNAIZ, Student ID: F118326
# Module: Introduction To Programming
# COURSEWORK: Library Management System
# Date: November 2021

from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figCanvas
import bookcheckout
import booksearch
import bookreturn
import bookrecommendations

# Instead of rewriting the message box color code multiple times, I created functions
def messageBoxRed():
    message_frame.config(bg="#FF8585")
    message_lbl.config(bg="#FF8585")
def messageBoxGreen():
    message_frame.config(bg="#84FF7C")
    message_lbl.config(bg="#84FF7C")
def messageBoxYellow():
    message_frame.config(bg="#F2F100")
    message_lbl.config(bg="#F2F100")

def returnBookWindow():
    bookID = bookIDReturn.get()             # Here we get the Tkinter Entry
    warningTextBox.delete('1.0', END)       # Clearing the warning textbox so that it doesnt accumulate
    if bookID != "":
        
        output, warning = bookreturn.returnBook(str(bookID))# Here we get the output from bookReturn.py
        if output == "Book returned!":      # If it was returned correctly then it will show that
            messageBoxGreen()
            message_lbl["text"] = str(output)
        elif output == "Warning":           # If the books has been overdue for more than 60 days then it will show that
            messageBoxYellow()
            message_lbl["text"] = "Book returned! [WARNING: Member has the following over-due books]"
            for index in range(0, len(warning)):# In this "for" loop it will add all the books that are overdue
                warningTextBox.insert(END, str(warning[index]) + "\n")
                
        # Otherwise errors output if the input data is wrong or if there were any other errors
        else:
            messageBoxRed()
            message_lbl["text"] = str(output)
    else:
        messageBoxRed()
        message_lbl["text"] = "Please enter a book ID"

def checkOutBookWindow():
    bookID = bookIDCheckOut.get()
    memberID = str(memberIDCheckOut.get())
    warningTextBox.delete('1.0', END)

    if bookID != "" and memberID != "":
        if len(memberID) == 4:
            output, warning = bookcheckout.checkOutBook(bookID, memberID)
            if output == "Book checked out!":   # If the book was checked out correctly it will show
                messageBoxGreen()
                message_lbl["text"] = str(output)
            elif output == "Warning":           # If the member has an overdue book it will show a warning message
                messageBoxYellow()
                message_lbl["text"] = "Book checked out! [WARNING: Member has " \
                                      "the following over-due books]"
                # In this "for" loop it will add all the books that are overdue
                for index in range(0, len(warning)):
                    warningTextBox.insert(END, str(warning[index]) + "\n")
            # Otherwise error messages will output
            else:
                messageBoxRed()
                message_lbl["text"] = str(output)
        else:
            messageBoxRed()
            message_lbl["text"] = "Please enter only 4 characters for the memeber ID"
    else:
        messageBoxRed()
        message_lbl["text"] = "Please enter book ID and memeber ID"

def searchBookWindow():
    bookEntry = searchEntry.get()
    warningTextBox.delete('1.0', END)
    if bookEntry != "":
        output, warning = booksearch.searchBook(bookEntry)
        if output == "Sorry, no book was found":        # Error message if no book was found
            messageBoxRed()
            message_lbl["text"] = output
        else:
            # Clearing the search text boxes so that they don't accumulate outputs
            searchTextBox.delete('1.0', END)
            warningTextBox.delete('1.0', END)
            if warning == []:
                messageBoxGreen()
                message_lbl["text"] = "Book(s) Found!"
            else:
                messageBoxYellow()
                message_lbl["text"] = "Book(s) Found! [WARNING: The following books are over-due]"
                # In this "for" loop it will add all the books that are overdue
                for index in range(0, len(warning)):
                    warningTextBox.insert(END, str(warning[index]) + "\n")
            for book in range(0, len(output)):
                searchTextBox.insert(END, str(output[book])+"\n")
    # Error message will output otherwise
    else:
        messageBoxRed()
        message_lbl["text"] = "Please enter a book ID"

def recommendWindow():
    memberEntry = memberID_recom_entry.get()
    graphTitle = []
    graphPoints =[]
    warningTextBox.delete('1.0', END)

    if memberEntry != "":
        if len(memberEntry) == 4:
            output, bookPoints = bookrecommendations.recommendBook(memberEntry)
            if output == []:
                messageBoxRed()
                message_lbl["text"] = "No recommended books found"
            else:
                recomTextBox.delete('1.0', END)
                messageBoxGreen()
                message_lbl["text"] = "Book(s) Found"
                for book in range(0, len(output)):             # Loop used to output all recommended books
                    recomTextBox.insert(END, str(output[book]) + "\n")
                # Once we have found books to recommend to the user we can create and plot the graph
                figure = plt.Figure(figsize=(4, 2))
                plotGraph = figCanvas(figure, recommend_frame)  # Where and what it will plot
                plotGraph.get_tk_widget().place(x=650, y=30)
                for points in range(0, len(bookPoints)):        # Graphing all the points
                    graphTitle.append(bookPoints[points][0])
                    graphPoints.append(int(bookPoints[points][1]))
                pieGraph = figure.add_subplot(1, 1, 1)
                pieGraph.set_title("Popularity Percentage")
                # Below I create the graph so that it matches the users likings
                pieGraph.pie(graphPoints, labels=graphTitle, autopct='%1.0f%%', radius= 1.1)
                plotGraph.draw()
        # Error messages again, below
        else:
            messageBoxRed()
            message_lbl["text"] = "Please enter only 4 characters for the memeber ID"
    else:
        messageBoxRed()
        message_lbl["text"] = "Please enter a member ID"



# COLORS
lbl_bg_color = "#A4A4A4"
frame_color = "#D6D6D6"

# Creating the main window
mainWindow = Tk()
mainWindow.title("Libary Management System")
mainWindow.geometry("1100x610")
title = Label(text="Library Management Sytem", width="600", height="1", bg=lbl_bg_color,
              font=("Arial", 20))
title.pack()

# message
# All the separate regions will be inside different frames in order to change the position of each item easily
message_frame = Frame(mainWindow, bg=frame_color, width="1060", height="68")
message_frame.place(x=20, y=520)
warning_frame = Frame(message_frame)
warning_frame.place(x=496, y=0)

# Each region has their own title to separate clearly
message_title = Label(message_frame, text="Messages will be displayed bellow: ",
                      width="70", fg="black", bg=lbl_bg_color, anchor="w")
message_title.place(x=0, y=0)

# Scroll bars are usefull when the info in each textbox doesn't fit
scrollBarWarning = Scrollbar(warning_frame, orient=VERTICAL)
scrollBarWarning.pack(fill=Y, side=RIGHT)       # This fills the y side on the right of the frame
warningTextBox = Text(warning_frame, bg="white", width="68", height="4",
                      yscrollcommand=scrollBarWarning.set)
warningTextBox.config(wrap='none') # This allows the text inside to not wrap and so we can scroll to see the rest
warningTextBox.pack()

# This label changes when each message is outputted (for example "Book returned")
message_lbl = Label(message_frame, bg=frame_color)
message_lbl.place(x=10, y=35)


# The following regions bellow are similar to the one described above, so not many comments will be made

# check out
checkOut_frame = Frame(mainWindow, bg=frame_color, width="400", height="120")
checkOut_frame.place(x=20, y=50)

checkOut_title = Label(checkOut_frame, text="Check Out Book (enter Book ID and Member ID): ",
                       width="75", fg="black", bg=lbl_bg_color, anchor="w")
checkOut_title.place(x=0, y=0)

checkOut_lbl_book = Label(checkOut_frame, text="Book ID: ", fg="black", bg=frame_color)
checkOut_lbl_book.place(x=10, y=40)
checkOut_lbl_memb = Label(checkOut_frame, text="Member ID: ", fg="black", bg=frame_color)
checkOut_lbl_memb.place(x=10, y=75)

# The entries collect a string variable which is then passed into the functions above
memberIDCheckOut = StringVar()
memberID_checkOut_entry = Entry(checkOut_frame, textvariable=memberIDCheckOut)
memberID_checkOut_entry.place(x=90, y=75)
bookIDCheckOut = StringVar()
bookID_checkOut_entry = Entry(checkOut_frame, textvariable=bookIDCheckOut)
bookID_checkOut_entry.place(x=90, y=40)

# Each button executes the functions above, the functions they execute are within the "command" attribute
btn_checkOut = Button(checkOut_frame, text="Check Out Book", width="15",
                      height="3", command=checkOutBookWindow)
btn_checkOut.place(x=250, y=40)


# return
return_frame = Frame(mainWindow, bg=frame_color, width="400", height="80")
return_frame.place(x=20, y=180)

return_title = Label(return_frame, text="Return Book (enter Book ID): ",
                     width="75", fg="black", bg=lbl_bg_color, anchor="w")
return_title.place(x=0, y=0)
return_lbl = Label(return_frame, text="Book ID: ", fg="black", bg=frame_color)
return_lbl.place(x=10, y=40)

bookIDReturn = StringVar()
bookID_return_entry = Entry(return_frame, textvariable=bookIDReturn)
bookID_return_entry.place(x=90, y=40)

btn_return = Button(return_frame, text="Return Book", width="15", height="2", command=returnBookWindow)
btn_return.place(x=250, y=30)


# search
search_frame = Frame(mainWindow, bg=frame_color, width="640", height="210")
search_frame.place(x=440, y=50)
searchOutputFrame = Frame(search_frame)
searchOutputFrame.place(x=5, y=70)

search_title = Label(search_frame, text="Search For Book (enter Title):",
                     width="91", fg="black", bg=lbl_bg_color, anchor="w")
search_title.place(x=0, y=0)
search_lbl = Label(search_frame, text="Enter Title: ", fg="black", bg=frame_color)
search_lbl.place(x=10, y=35)

searchEntry = StringVar()
search_entry = Entry(search_frame, width="28", textvariable=searchEntry)
search_entry.place(x=85, y=35)

scrollBarSearchX = Scrollbar(searchOutputFrame, orient=HORIZONTAL)
scrollBarSearchY = Scrollbar(searchOutputFrame, orient=VERTICAL)
scrollBarSearchY.pack(fill=Y, side=RIGHT)
scrollBarSearchX.pack(fill=X, side=BOTTOM)
searchTextBox = Text(searchOutputFrame, bg="white", width="76", height="7",
                     xscrollcommand=scrollBarSearchX.set, yscrollcommand=scrollBarSearchY.set)
searchTextBox.config(wrap='none')
searchTextBox.pack()
scrollBarSearchX.config(command=searchTextBox.xview)
scrollBarSearchY.config(command=searchTextBox.yview)

btn_search_title = Button(search_frame, text="Search", width="15", command=searchBookWindow)
btn_search_title.place(x=280, y=32)


# recommendations
recommend_frame = Frame(mainWindow, bg=frame_color, width="1060", height="240")
recommend_frame.place(x=20, y=270)
recomoutputFrame = Frame(recommend_frame)
recomoutputFrame.place(x=8, y=65)

recom_title = Label(recommend_frame, text="Books recommended (enter Member ID): ",
                    width="190", fg="black", bg=lbl_bg_color, anchor="w")
recom_title.place(x=0, y=0)

search_lbl = Label(recommend_frame, text="Member ID: ", fg="black", bg=frame_color)
search_lbl.place(x=10, y=35)

memberID_recom_entry = StringVar()
memberID_recom_entry = Entry(recommend_frame, textvariable=memberID_recom_entry)
memberID_recom_entry.place(x=90, y=35)

scrollBarRecomY = Scrollbar(recomoutputFrame, orient=VERTICAL)
scrollBarRecomX = Scrollbar(recomoutputFrame, orient=HORIZONTAL)
scrollBarRecomY.pack(fill=Y, side=RIGHT)
scrollBarRecomX.pack(fill=X, side=BOTTOM)
recomTextBox = Text(recomoutputFrame, bg="white", width="76", height="9",
                    yscrollcommand=scrollBarRecomY.set, xscrollcommand=scrollBarRecomX.set)
recomTextBox.config(wrap='none')
recomTextBox.pack()
scrollBarRecomX.config(command=recomTextBox.xview)
scrollBarRecomY.config(command=recomTextBox.yview)

btn_search = Button(recommend_frame, text="Search", width="15", height="1", command=recommendWindow)
btn_search.place(x=250, y=30)


mainloop()
