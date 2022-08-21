# MARIO PORTILLO HERNAIZ
# Date: November 2021

import database

def checkOutBook(bookID, memberID):
    # Importing data from the database
    bookFound = database.searchForBook(bookID)
    listOfBooks = database.getBookList()
    warningList = []
    # First I check that the book that was entered exists in the database
    if bookFound != []:
        # Now we check that the existen book has not been checked out
        if bookFound[5] == "0":
            # If it hasn't been checked out then we change data in the files
            bookFound[5] = str(memberID)
            database.writeOnDatabase(bookFound, bookID)
            database.writeOnLog(bookFound, memberID, "checkOut")
            bookMoreThan60 = database.checkIfDaysOnLoanIs60(memberID, "member")
            # Here I make sure that any of the memeber's books have not been checked out for more than 60 days
            if bookMoreThan60 == []:
                # If it hasnt, it will just return the message string
                return "Book checked out!", []
            else:
                warningList.append("Overdue:")
                # If it has then it will create a warning list with all the book the member has checked out
                # for more than 60 days
                for overDue in range(0, len(bookMoreThan60)):
                    for book in range(0, len(listOfBooks)):
                        if bookMoreThan60[overDue]==listOfBooks[book][0]:
                            warningList.append("ID: %s - Title: %s - Author: %s"
                                              % (listOfBooks[book][0], listOfBooks[book][2], listOfBooks[book][3]))
                return "Warning", warningList
        # Error messages will be returned
        else:
            return ("Sorry, this book has already been checked out by " + bookFound[5]), []
    else:
        return "Sorry the book you are searching for doesn't exist", []

# TEST CODE 

if __name__ == "__main__":      
    # 1) Correct Inputs
    print(checkOutBook("3", "test"))
    
    # 2) Incorrect Book ID
    print(checkOutBook("20", "test"))
    
    # 3) Already Checked Out Book
    print(checkOutBook("14", "test"))
    
    # 4) Warning Output
    print(checkOutBook("2", "mari"))
