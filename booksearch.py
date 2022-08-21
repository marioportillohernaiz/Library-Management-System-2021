# MARIO PORTILLO HERNAIZ, Student ID: F118326
# Date: November 2021

import database

def searchBook(searchBook):
    listOfBooks = database.getBookList()
    bookMoreThan60 = database.checkIfDaysOnLoanIs60(searchBook, "title")
    bookFound=[]
    returnList = []
    warningList = []

    # Firstly we create a list with all the books found (same titles with different ID's)
    for book in listOfBooks:
        if book[2] == searchBook:
            bookFound.append(book)

    if bookFound != []:
        # If the bookFound list is not empy then it means it found a book(s) so we create our output strin
        returnList.append("There were " + str(len(bookFound)) + " copies found:")
        for book in range(0, len(bookFound)):
            # For each book that was found, if it has "0" then it means it is available otherwise its not
            if bookFound[book][5] == "0":
                availability = "Available"
            else:
                availability = "Not Available"
            # The returnList returns a string with all the data of each book
            returnList.append(("ID: %s - Book: %s - Author: %s - Genre: %s - Purchase Date: %s - Availability: %s")\
                            %(bookFound[book][0], bookFound[book][2], bookFound[book][3], bookFound[book][1],
                              bookFound[book][4], availability))
        # If any of the books was on loan for more than 60 days then it will output the data of that book.
        # Otherwise it will return an empty string which means there were no over due books
        if bookMoreThan60 == []:
            return returnList, []
        else:
            warningList.append("Overdue:")
            for overDue in range(0, len(bookMoreThan60)):
                for book in range(0, len(listOfBooks)):
                    if bookMoreThan60[overDue] == listOfBooks[book][0]:
                        warningList.append("ID: %s - Title: %s - MemberID: %s"
                                           % (listOfBooks[book][0], listOfBooks[book][2], listOfBooks[book][5]))
            return returnList, warningList
    # If the book wasn't found then an error will output
    else:
        return "Sorry, no book was found", []

# TEST CODE

if __name__ == "__main__":
    # 1) Book IN database
    print(searchBook("Gone"))
    
    # 2) Book NOT in database
    print(searchBook(""))
    print(searchBook("Harry Potter"))
    
    # 3) Book with more than 60 days overdue
    print(searchBook("War And Peace"))
