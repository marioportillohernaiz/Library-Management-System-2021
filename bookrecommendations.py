# MARIO PORTILLO HERNAIZ
# Date: November 2021

import database

def recommendBook(memberID):
    # Importing all the data from the database and creating all the lists needed
    listOfLogs = database.getLogList()
    listOfBooks = database.getBookList()
    booksLogCount = database.getNumOfBookLoans()
    listOfGenres = []
    reccomBooks = []
    returnList = []
    repeatedTitles = []
    topBooks = []
    bookPoints = []
    memberExists = False

    # Looping through the log list to check if the member exists.
    for log in range(0, len(listOfLogs)):
        if listOfLogs[log][3] == memberID:
            memberExists = True

    # If the member exists then we can recommend them books depending on their log history.
    if memberExists == True:

        # Here I make sure that both the book ID and member ID match in both Log list and
        # database list (book list). Then I add the genre of that book to a list of genres.
        for log in range(0, len(listOfLogs)):
            for book in range(0, len(listOfBooks)):
                if listOfBooks[book][0]==listOfLogs[log][1] and listOfLogs[log][3]==memberID and \
                        listOfBooks[book][1] not in listOfGenres:
                    listOfGenres.append(listOfBooks[book][1])

        # The following loop adds any books that have the same or similar genre to the books the member has
        # previously check out.
        for genre in range(0, len(listOfGenres)):
            for book in range(0, len(listOfBooks)):
                # Books with the same genre
                if (listOfGenres[genre]==listOfBooks[book][1]) and (listOfBooks[book][2] not in reccomBooks):
                        reccomBooks.append(listOfBooks[book][2])

                # As there are not enough books with the same genre, I will recommend genre's that are similar.
                if (listOfGenres[genre]=="Fiction" and listOfBooks[book][1]=="Action") and \
                        (listOfBooks[book][2] not in reccomBooks):
                    reccomBooks.append(listOfBooks[book][2])
                if (listOfGenres[genre]=="Drama" and listOfBooks[book][1]=="Romance") and \
                        (listOfBooks[book][2] not in reccomBooks):
                    reccomBooks.append(listOfBooks[book][2])
                if (listOfGenres[genre]=="Non Fiction" and listOfBooks[book][1]=="Selfhelp") and \
                        (listOfBooks[book][2] not in reccomBooks):
                    reccomBooks.append(listOfBooks[book][2])

        # Once I have all the book titles I loop through the recommended book list and add
        # the book "points" (or number of checked out books) to each recommended book.
        # As the log count is sorted, I will loop through the list so that the top books
        # are appended in order of most points.
        for count in range(0, len(booksLogCount)):
            for book in range(0, len(reccomBooks)):
                if booksLogCount[count][0]==reccomBooks[book]:
                    topBooks.append(reccomBooks[book])

        # Here I make sure that the number of top recommended books are in the range of 3 to 10
        if len(topBooks)>=3 and len(topBooks)<=10:
            returnList = createRecomBooks(topBooks)
        elif len(topBooks)<3:
            # If the list has less than 3 books then it will add the 3 top books as well
            for i in range(0, 3):
                if booksLogCount[i][0] not in topBooks:
                    topBooks.append(booksLogCount[i][0])
            returnList = createRecomBooks(topBooks)
        else:
            # If the list has more than 10 books then it will remove books until the list has 10
            for i in range(0, len(topBooks)):
                if len(topBooks)>10:
                    topBooks.pop(-1)
            returnList = createRecomBooks(topBooks)

    # If the member doesn't exist then they will get recommended 5 of the most checked out books
    else:
        for i in range(0, 5):
            topBooks.append(booksLogCount[i][0])
        returnList = createRecomBooks(topBooks)

    # Here I create a points list of the most checked out books that are in the member's
    # list, to plot on the Matplotlib graph
    for book in range(0, len(topBooks)):
        for count in range(0, len(booksLogCount)):
            if str(topBooks[book]) == str(booksLogCount[count][0]):
                bookAndPoints = booksLogCount[count][0], booksLogCount[count][1]
                bookPoints.append(bookAndPoints)

    return returnList, bookPoints

def createRecomBooks(topBooks):
    listOfBooks = database.getBookList()
    returnList = []
    repeatedTitles = []

    # Each time this function is called I loop through the recommended top books and create the desied
    # string that returns to the menu.py
    returnList.append("Found " + str(len(topBooks)) + " recommended books:")
    for top in range(0, len(topBooks)):
        for book in range(0, len(listOfBooks)):
            if (topBooks[top] == listOfBooks[book][2]) and (topBooks[top] not in repeatedTitles):
                repeatedTitles.append(topBooks[top])
                returnList.append("Book Title: %s - Author: %s - Genre: %s"
                                  % (listOfBooks[book][2], listOfBooks[book][3], listOfBooks[book][1]))
    return returnList

# TEST CODE

if __name__ == "__main__":
    # "recommendBook"
    # 1) Existing User
    print(recommendBook("test"))
    
    # 2) Non-existing User
    print(recommendBook("aaaa"))

    # "createRecomBooks"
    # 1) The only input is a list of book titles of length 3 to 10
    print(createRecomBooks(['War And Peace', 'Gone', 'Atomic Habits', "Corrupt"]))
