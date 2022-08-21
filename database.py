# MARIO PORTILLO HERNAIZ
# Date: November 2021

import datetime
from datetime import timedelta
from datetime import datetime

# Instead of writing the text files multiple times I decided to create global variables
globalDatabase = "database.txt"
globalLog = "log.txt"

def getBookList():
    splitListOfBooks=[]  # Creating lists to use
    listOfBooks=[]
    returnList=[]
    dataFile = open(globalDatabase, "r")  # Opening and reading the database

    for data in dataFile:
        splitListOfBooks += data.split("\n")  # For some reason the list contains "\n" so I'm taking it out

    for book in range(0, len(splitListOfBooks)):
        if splitListOfBooks[book] != "":                       # The list also contains spaces so I'm skipping them
            listOfBooks = splitListOfBooks[book].split("~")    # Taking "~" off the datalist aswell
            returnList.append(listOfBooks)                  # Adding desired output of books to the return list
    dataFile.close()
    return returnList

def getLogList():
    splitListOfLogs=[]  # Creating lists to use
    listOfLogs=[]
    returnList=[]
    dataFile = open(globalLog, "r")  # Opening and reading the database

    for data in dataFile:
        splitListOfLogs += data.split("\n")  # For some reason the list contains "\n" so I'm taking it out

    for book in range(0, len(splitListOfLogs)):
        if splitListOfLogs[book] != "":                       # The list also contains spaces so I'm skipping them
            listOfLogs = splitListOfLogs[book].split("~")     # Taking "~" off the datalist aswell
            returnList.append(listOfLogs)                  # Adding desired output of logs to the return list
    dataFile.close()
    return returnList

def writeOnDatabase(borrowedBook, bookID):
    listOfBooks=getBookList()
    bookInfo = ""
    dataFile = open(globalDatabase, "w")  # Opening and writting in the database file

    # Looping through the file. If the book ID matches with the parameter then add that book,
    # if not then add the books that where alreay in the database.
    for book in range(0, len(listOfBooks)):
        if listOfBooks[book][0] == bookID:
            bookInfo = "~".join(borrowedBook) + "\n"
            dataFile.write(bookInfo)
        else:
            bookInfo = "~".join(listOfBooks[book]) + "\n"
            dataFile.write(bookInfo)
    dataFile.close()

def writeOnLog(bookFound, memberID, typeOfWrite):
    dateNow = datetime.now()
    formatDate = dateNow.strftime("%d/%m/%Y")
    listOfLogs = getLogList()
    count=0
    memberName=""
    logFile = open(globalLog, "a+")     # Opening the file to append and read items

    # If we are checking out we can easily add the member ID and the book ID and then append the log to the log list
    if typeOfWrite == "checkOut":
        writeLog = "CHECKOUT~"+str(bookFound[0])+"~"+str(bookFound[2])+"~"+str(memberID)+"~"+str(formatDate)+"\n"
        logFile.write(writeLog)
    else:
        # When returning a book, because we don't have a member ID, I loop through the log list to find the book
        # ID that corresponds to the book being returned. Then I get the last member who borrowed it.
        for log in range(0, len(listOfLogs)):
            if listOfLogs[log][1] == bookFound[0]:
                memberName = str(listOfLogs[log][3])
                count+=1

        # For every book I find, I add a count and so I make sure the count is odd, meaning the book has been checked
        # out and returned an even number of times PLUS the last time it was checked out, leaving an odd count.
        if count % 2 != 0:
            writeLog = "RETURN~"+str(bookFound[0])+"~"+str(bookFound[2])+"~"+memberName+"~"+str(formatDate)+"\n"
            logFile.write(writeLog)
    logFile.close()

def searchForBook(bookID):
    # In this function I search for the book ID and make sure that is available for loan in the database list
    bookFound = []
    availableBooks = 0
    listOfBooks = getBookList()

    for book in listOfBooks:
        if book[0] == bookID:
            availableBooks += 1
            bookFound = book
            return bookFound
        else:
            # If we reach the end of the list (where the last book ID equals the length of the book list) and
            # we still have 0 available books then an empty string is returned meaning no boook was found
            if book[0] == str(len(listOfBooks)) and availableBooks == 0:
                return []

def checkIfDaysOnLoanIs60(ID, typeOfID):
    listOfLogs = getLogList()
    dateNow = datetime.now()
    returnList = []
    member = ""
    plus60Days = ""

    # There are 3 ways of checking the loan date, using the member ID, the book ID or the title of the book
    if typeOfID=="member":
        # If we have the member ID we can loop through the log list and check is the inputed member
        # has any books loaned for more than 60 days.
        for log in range(0, len(listOfLogs)):
            logTimeObj = datetime.strptime(listOfLogs[log][4], "%d/%m/%Y")
            plus60Days = logTimeObj + timedelta(days=60)
            # If the loaned date is smaller (or still in the past after 60 days) then it means it has been
            # checked out for more than 60 days. Also we can only get this book if the ID's match
            if dateNow>=plus60Days and listOfLogs[log][3]==ID and listOfLogs[log][0]=="CHECKOUT":
                returnList.append(listOfLogs[log][1])
    elif typeOfID=="book":
        # Here we have the book ID but we still follow the process above.
        member = listOfLogs[len(listOfLogs)-1][3]
        for log in range(0, len(listOfLogs)):
            logTimeObj = datetime.strptime(listOfLogs[log][4], "%d/%m/%Y")
            plus60Days = logTimeObj + timedelta(days=60)
            diffInDays = dateNow - logTimeObj
            if dateNow>=plus60Days and listOfLogs[log][3]==member and listOfLogs[log][0]=="CHECKOUT":
                returnList.append([listOfLogs[log][1], diffInDays.days])
    else:
        # Same for the Title book, we follow the process from above.
        for log in range(0, len(listOfLogs)):
            logTimeObj = datetime.strptime(listOfLogs[log][4], "%d/%m/%Y")
            plus60Days = logTimeObj + timedelta(days=60)
            if dateNow >= plus60Days and listOfLogs[log][2]==ID and listOfLogs[log][0]=="CHECKOUT":
                returnList.append(listOfLogs[log][1])
    return returnList

def getNumOfBookLoans():
    listOfLogs = getLogList()
    listOfBooks = getBookList()
    listOfTitles = []
    bookCount = {}
    countOfLoans=0

    # Firstly to make it easier I loop through the list of books and get a list of all the book titles
    for book in range(0, len(listOfBooks)):
        if listOfBooks[book][2] not in listOfTitles:
            listOfTitles.append(listOfBooks[book][2])

    # Now for each book, we add a point to each check out and then add it to a list as tuples.
    for title in range(0, len(listOfTitles)):
        countOfLoans=0
        for log in range(0, len(listOfLogs)):
            if listOfLogs[log][0] == "CHECKOUT":
                if listOfLogs[log][2]==listOfTitles[title]:
                    countOfLoans+=1
                    bookCount[listOfTitles[title]] = countOfLoans

    # Before returning the list we sort it by points
    sortReturn = sorted(bookCount.items(), key=lambda x:x[1], reverse=True)
    return sortReturn

# TEST CODE

if __name__ == "__main__":
    # "getBookList"
    # 1) Outputing book list
    print(getBookList())

    # "getLogList"
    # 1) Outputing log list
    print(getLogList())

    # "writeOnDatabase" AND "writeOnLog"
    # Both test codes have to be made at the same time or else the databases clash. This is because once
    # a book has been checked out it needs to be changed in both the log and the database lists.
    # 1) Correct input. It does not return anything, but you should be able to see a change in the files
    writeOnDatabase(['3', 'Selfhelp', 'Atomic Habits', 'James Clear', '02/01/2021', 'test'], "3")
    writeOnLog(['3', 'Selfhelp', 'Atomic Habits', 'James Clear', '02/01/2021', 'test'], "test", "checkOut")

    # 2) Another Correct input
    writeOnDatabase(['3', 'Selfhelp', 'Atomic Habits', 'James Clear', '02/01/2021', '0'], "3")
    writeOnLog(['3', 'Selfhelp', 'Atomic Habits', 'James Clear', '02/01/2021', 'test'], "test", "return")

    # "searchForBook"
    # 1) Correct input
    print(searchForBook("3"))
    
    # 2) Incorrect input
    print(searchForBook("17"))

    # "checkIfDaysOnLoanIs60"
    # 1) No 60 days
    print(checkIfDaysOnLoanIs60("test", "member"))
    print(checkIfDaysOnLoanIs60("3", "book"))
    print(checkIfDaysOnLoanIs60("Atomic Habits", "search"))
          
    # 2) 60 days check out
    print(checkIfDaysOnLoanIs60("mari", "member"))
    print(checkIfDaysOnLoanIs60("1", "book"))
    print(checkIfDaysOnLoanIs60("War And Peace", "search"))

    # "getNumOfBookLoans"
    print(getNumOfBookLoans())
