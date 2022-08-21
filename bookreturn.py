# MARIO PORTILLO HERNAIZ
# Date: November 2021

import database

def returnBook(bookID):
    # Importing data from the database
    bookFound = database.searchForBook(bookID)
    listOfBooks = database.getBookList()
    warningList = []
    # First I check that the book that was entered exists in the database
    if bookFound != []:
        # Now we check that the existen book has been checked out
        if bookFound[5] != "0":
            # If it has been checked out then we change data in the files
            bookFound[5] = "0"
            database.writeOnDatabase(bookFound, bookID)
            database.writeOnLog(bookFound, "", "return")
            bookMoreThan60 = database.checkIfDaysOnLoanIs60(bookID, "book")
            # Here I make sure that any of the memeber's books have not been checked out for more than 60 days
            if bookMoreThan60 == []:
                # If it hasnt, it will just return the message string
                return "Book returned!", []
            else:
                warningList.append("Overdue:")
                # If it has then it will create a warning list with all the book the member has checked out
                # for more than 60 days
                for overDue in range(0, len(bookMoreThan60)):
                    for book in range(0, len(listOfBooks)):
                        if bookMoreThan60[overDue][0]==listOfBooks[book][0]:
                            warningList.append("Book ID: %s - Title: %s - Days over-due: %s days"
                                              % (listOfBooks[book][0], listOfBooks[book][2],
                                                 bookMoreThan60[overDue][1]))
                return "Warning", warningList
        # Error messages will be returned
        else:
            return "Sorry, this book has not been checked out", []
    else:
        return "Sorry the book you are searching for doesn't exist", []

# TEST CODE

if __name__ == "__main__":
    # 1) Correct Inputs
    print(returnBook("8"))
    
    # 2) Incorrect Book ID
    print(returnBook("20"))
    
    # 3) Already Returned Book
    print(returnBook("17"))
    
    # 4) Warning Output
    print(returnBook("7"))
