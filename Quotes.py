from bs4 import BeautifulSoup as bs 
import requests
import time
import mysql.connector
from mysql.connector import errorcode


def ConnectToDatabase():
    cnxn = None
    try:
        cnxn = mysql.connector.connect(user='root', password='Admin!42', database='quotescrawler')
        print('Connected to database.')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return cnxn


def CloseConnectionToDatabase(cnxn, cursor):
    try:
        cursor.close()
        cnxn.close()
        print('Connection closed to database.')
    except:
        print('Failed to close database connection.')
        return False
    return True


def GetPage(page):
    r = requests.get(website + "/page/{}/".format(page))
    print("Page {} requested.".format(page))
    return bs(r.text,'html.parser')

def FindNextPage(Webpage):
    return Webpage.find('li',attrs={'class':'next'}) != None

def ScrapeQuotePairs(soup):
    return soup.find_all('div', attrs={'class':'quote'})


def GetAuthor(quotes):
    return quotes.find('small', attrs={'class':'author'}).get_text()

def GetAuthorDescription(quotePair):
    link = quotePair.find('a')
    r = requests.get(website + link['href'])
    soup = bs(r.text, 'html.parser')
    return soup.find('div', attrs={'class':'author-description'}).get_text().strip()


def FindAuthorIDInDb(cursor, name):
    query = "SELECT author_id FROM authors WHERE name = '{}'".format(name.replace("'", "\\'"))
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err)
    if cursor.rowcount != 0:
        print('{} found in server.'.format(name))
        return cursor._rows[0][0]
    else:
        print('{} not found in server.'.format(name))
        return None

def AddAuthorToDb(cnxn, cursor, quotePair):
    query = "INSERT INTO authors (name, description) VALUES (%s, %s)"
    author = GetAuthor(quotePair)
    authorInfo = (author, GetAuthorDescription(quotePair))

    try:
        cursor.execute(query, authorInfo)
        cnxn.commit()
        print("Added {} to the database.".format(author))
    except mysql.connector.Error as err:
        print(err)


def GetQuoteText(quotePair):
    return quotePair.find('span', attrs={'class':'text'}).get_text()

def FindQuoteInDb(cursor, quoteText):
    query = "SELECT * FROM quotes WHERE quote = '{}'".format(quoteText.replace("'", "\\'"))
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err)

    if cursor.rowcount == 0:
        print("Quote not found in database.")
        return False
    else:
        print("Quote found in database")
        return True

def AddQuoteToDb(cnxn, cursor, authorID, quoteText):
    try:
        query = "INSERT INTO quotes (author_id, quote) VALUES (%s, %s)"
        quoteValues = (authorID, quoteText)
        cursor.execute(query, quoteValues)
        cnxn.commit()
        print("Added quote to database")
    except mysql.connector.Error as err:
        print(err)


def crawl(cnxn, cursor):
    pageIndex = 1
    while True:
        Webpage = GetPage(pageIndex)
        quotePairs = ScrapeQuotePairs(Webpage)
        for i in range(len(quotePairs)):
            quoteText = GetQuoteText(quotePairs[i])
            if FindQuoteInDb(cursor, quoteText):
                continue

            authorID = FindAuthorIDInDb(cursor, GetAuthor(quotePairs[i]))
            time.sleep(1)
            if authorID == None:
                AddAuthorToDb(cnxn, cursor, quotePairs[i])
                time.sleep(1)
                authorID = FindAuthorIDInDb(cursor, GetAuthor(quotePairs[i]))
                time.sleep(1)

            AddQuoteToDb(cnxn, cursor, authorID, quoteText)
            time.sleep(2)
        if FindNextPage(Webpage):
            pageIndex += 1
        else:
            break
        time.sleep(2)
    print("Finished scraping")


def main():
    cnxn = ConnectToDatabase()
    cursor = cnxn.cursor(buffered=True)

    if(cnxn.is_connected):
        try:
            crawl(cnxn, cursor)
        except mysql.connector.Error as err:
            print(err)

    if (cnxn.is_connected):
        CloseConnectionToDatabase(cnxn, cursor)


website = 'http://quotes.toscrape.com/'
main()
