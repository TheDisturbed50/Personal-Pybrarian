import webbrowser
import requests
import sqlite3
import random
import csv
from tkinter import Tk, filedialog

app_title = """
.....########..########.########...######...#######..##....##....###....##.........
.....##.....##.##.......##.....##.##....##.##.....##.###...##...##.##...##.........
.....##.....##.##.......##.....##.##.......##.....##.####..##..##...##..##.........
.....########..######...########...######..##.....##.##.##.##.##.....##.##.........
.....##........##.......##...##.........##.##.....##.##..####.#########.##.........
.....##........##.......##....##..##....##.##.....##.##...###.##.....##.##.........
.....##........########.##.....##..######...#######..##....##.##.....##.########...
.########..##....##.########..########.....###....########..####....###....##....##
.##.....##..##..##..##.....##.##.....##...##.##...##.....##..##....##.##...###...##
.##.....##...####...##.....##.##.....##..##...##..##.....##..##...##...##..####..##
.########.....##....########..########..##.....##.########...##..##.....##.##.##.##
.##...........##....##.....##.##...##...#########.##...##....##..#########.##..####
.##...........##....##.....##.##....##..##.....##.##....##...##..##.....##.##...###
.##...........##....########..##.....##.##.....##.##.....##.####.##.....##.##....##
\n\n"""
app_subtitle = ["Hosting book-buying interventions since 2022!\n\n\n",
                "Settle those arguments about your book addiction!\n\n\n",
                "If you know at least 3 words in Elvish, your in the right place.\n\n\n",
                "Yes, you were seen sniffing those book pages...\n\n\n",
                "Do we need to check your kindle, too???\n\n\n"]
db = sqlite3.connect("data/books.db")
cursor = db.cursor()


def data_fetch(url2):
    # url1 = "https://openlibrary.org/api/books?bibkeys=ISBN:"
    # url3 = "&jscmd=details&format=json"
    url1 = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    api_key = "AIzaSyBub1PyEefimXbWPBLrjGhM1PNuP1LQP14"
    url3 = "&key=" + api_key
    url = url1 + url2  # + url3  # concat url sections together, ISBN num passed through func arg
    print("API URI, GET Method: " + url + "\n")
    response = requests.request("GET", url)
    rparse = response.json()
    return rparse


def db_init():
    global db
    global cursor
    table = """ CREATE TABLE IF NOT EXISTS BOOKS(
                    ISBN VARCHAR(13) NOT NULL PRIMARY KEY,
                    title VARCHAR,
                    authors VARCHAR,
                    publisher VARCHAR,
                    publishedDate VARCHAR,
                    description VARCHAR,
                    pageCount VARCHAR,
                    categories VARCHAR,
                    averageRating VARCHAR,
                    smallThumbnail VARCHAR,
                    location VARCHAR
                ); """
    cursor.execute(table)
    print("Table is Ready")
    db.commit()


def man_add_mode(isbn, loop_override, loc="N/A"):  # CLI function for hard-keyed data
    print("Manual Add Mode started...\n\nPlease type book data as prompted, then press the Enter (Return) key.\n\n")

    if loc == "N/A":
        loc = input("Set the location of the Book Scans:\n> ")
        print(loc, " recorded")
    loop = True
    while loop is True:
        bk_isbn = isbn
        print("...ISBN ", bk_isbn, " recorded")
        bk_title = input("Title:  ")
        print(bk_title, " recorded")
        bk_auth = input("Author:  ")
        print(bk_auth, " recorded")
        bk_snippet = input("Description / Snippet:  ")
        print(bk_snippet, " recorded")
        bk_pub = input("Publisher/Company:  ")
        print(bk_pub, " recorded")
        bk_pubdate = input("Published Date:  ")
        print(bk_pubdate, " recorded")
        bk_pages = input("Pages:  ")
        print(bk_pages, " recorded")
        bk_cat = input("Category:  ")
        print(bk_cat, " recorded")
        bk_avgrate = "N/A"
        bk_thumb = "N/A"
        db_update(int(isbn), bk_title, bk_auth, bk_pub, bk_pubdate, bk_snippet,
                  bk_pages, bk_cat, bk_avgrate, bk_thumb, loc)
        print("...Book " + bk_title + " has been added!")
        if loop_override is True:
            loop = False
        cont = input("\nContinue adding books manually? (y)es or (n)o\n>").lower()
        if cont != "y" or "yes":
            loop = False


def scanner(auto_add=False):  # CLI function for ISBN searches/scans using API lookups
    print("Scanner started...")

    loc = input("Set the location of the Book Scans:\n> ")

    while True:
        print("Enter 'x' to stop at any time")
        isbn = input("Enter ISBN Number:\n> ")
        if isbn == "x":
            print("Scanner Stopped...")
            break

        book = data_fetch(isbn)  # Calls API and returns dict
        try:
            book_items = book["items"][0]
            volumeInfo = book_items["volumeInfo"]
            bk_snippet = book_items["searchInfo"]["textSnippet"]

            try:  # Error handle every key/val pair to keep program from imploding...
                bk_title = volumeInfo["title"]
            except:
                bk_title = "N/A"
            try:
                bk_auth = volumeInfo["authors"][0]
            except:
                bk_auth = "N/A"
            try:
                bk_pub = volumeInfo["publisher"]
            except:
                bk_pub = "N/A"
            try:
                bk_pubdate = volumeInfo["publishedDate"]
            except:
                bk_pubdate = "N/A"
            try:
                bk_pages = volumeInfo["pageCount"]
            except:
                bk_pages = "N/A"
            try:
                bk_cat = volumeInfo["categories"][0]
            except:
                bk_cat = "N/A"
            try:
                bk_avgrate = volumeInfo["averageRating"]
            except:
                bk_avgrate = "N/A"
            try:
                bk_thumb = volumeInfo["imageLinks"]["smallThumbnail"]
            except:
                bk_thumb = "N/A"
            print("Book Location: ", loc)
            print(int(isbn))
            print(bk_title)
            print(bk_auth)
            print(bk_pub)
            print(bk_pubdate)
            print(bk_snippet)
            print(bk_pages)
            print(bk_cat)
            print(bk_avgrate)
            print(bk_thumb)
            db_update(int(isbn), bk_title, bk_auth, bk_pub, bk_pubdate, bk_snippet,
                      bk_pages, bk_cat, bk_avgrate, bk_thumb, loc)
        except:
            print("\nNO BOOKS FOUND WITH ISBN: ", isbn)
            if auto_add is False:
                manual_prompt = input("\nDo you want to type this book info in MANUALLY? (y)es or (n)o\n>").lower()
                if manual_prompt == "y" or "yes":
                    man_add_mode(isbn, True, loc)
            else:
                bk_title = "N/A"  # setting NA values so it adds the record, and it can be edited/removed later on...
                bk_auth = "N/A"
                bk_pub = "N/A"
                bk_pubdate = "N/A"
                bk_snippet = "N/A"
                bk_pages = "N/A"
                bk_cat = "N/A"
                bk_avgrate = "N/A"
                bk_thumb = "N/A"
                db_update(int(isbn), bk_title, bk_auth, bk_pub, bk_pubdate, bk_snippet,
                          bk_pages, bk_cat, bk_avgrate, bk_thumb, loc)
                print("Added Blank entry with ISBN for follow-up...\n")


def retriever(isbn_arg=""):
    print("Searcher started...")
    if isbn_arg != "":
        isbn = isbn_arg

    while True:
        if isbn_arg == "":
            print("""
            Enter below the ISBN of the Book you need to edit.
            """)
            print("Enter 'x' to stop at any time")
            isbn = input("Enter ISBN Number:\n> ")
            if isbn == "x":
                print("Searcher Stopped...")
                break
        else:
            isbn = isbn_arg

        try:
            cursor.execute("SELECT * FROM BOOKS WHERE ISBN=?", (isbn,))
            row = cursor.fetchone()
            bk_title = row[1]
            bk_auth = row[2]
            bk_pub = row[3]
            bk_pubdate = row[4]
            bk_snippet = row[5]
            bk_pages = row[6]
            bk_cat = row[7]
            bk_avgrate = row[8]
            bk_thumb = row[9]
            loc = row[10]
        except Exception as e:
            print("Cannot find ISBN! Aborting operation...")
            print("Error Detail: ", e)
            break

        while True:
            print("""\n\nBook ISBN Selected: {}
            Choose an option to Edit:
            1 - Title ({})
            2 - Author ({})
            3 - Publisher ({})
            4 - Publish Date ({})
            5 - Description ({})
            6 - Pages ({})
            7 - Category ({})
            8 - Avg Rating ({})
            9 - Location ({})
            
            x - Exit
            """.format("\033[1;33m"+isbn+"\033[1;m", "\033[1;33m"+bk_title+"\033[1;m", "\033[1;33m"+bk_auth+"\033[1;m",
                       "\033[1;33m"+bk_pub+"\033[1;m", "\033[1;33m"+bk_pubdate+"\033[1;m",
                       "\033[1;33m"+bk_snippet+"\033[1;m", "\033[1;33m"+bk_pages+"\033[1;m",
                       "\033[1;33m"+bk_cat+"\033[1;m", "\033[1;33m"+bk_avgrate+"\033[1;m", "\033[1;33m"+loc+"\033[1;m"))
            sel = input("Selection:\n> ").lower()
            if sel == "1":
                bk_title = input("Title: ")
            elif sel == "2":
                bk_auth = input("Author: ")
            elif sel == "3":
                bk_pub = input("Publisher: ")
            elif sel == "4":
                bk_pubdate = input("Publish Date: ")
            elif sel == "5":
                bk_snippet = input("Description: ")
            elif sel == "6":
                bk_pages = input("Pages: ")
            elif sel == "7":
                bk_cat = input("Category: ")
            elif sel == "8":
                bk_avgrate = input("Average Rating: ")
            elif sel == "9":
                loc = input("Location: ")
            elif sel == "x":
                db_update(int(isbn), bk_title, bk_auth, bk_pub, bk_pubdate, bk_snippet,
                          bk_pages, bk_cat, bk_avgrate, bk_thumb, loc)
                print("DB update posted.")
                break
            else:
                print("Selection not recognised, please choose again!\n")

        if isbn_arg != "":
            break


def view_all():  # CLI function to list books (and count)
    global cursor
    print("Viewer started...")
    cursor.execute('SELECT * FROM BOOKS')
    data = cursor.fetchall()
    c = 1
    for row in data:
        print("#", c, " ", row)
        c = c + 1
    print("\nViewer finished...")


def db_update(i, t, a, p, pd, s, pg, c, r, tn, loc):  # method to add data from multiple call sources
    global db
    global cursor
    print("DB Update started...")
    cursor.execute("""INSERT OR REPLACE INTO BOOKS VALUES (
        :ISBN,
        :title,
        :authors,
        :publisher,
        :publishedDate,
        :description,
        :pageCount,
        :categories,
        :averageRating,
        :smallThumbnail,
        :location
    )""", *[{
        "ISBN": i,
        "title": t,
        "authors": a,
        "publisher": p,
        "publishedDate": pd,
        "description": s,
        "pageCount": pg,
        "categories": c,
        "averageRating": r,
        "smallThumbnail": tn,
        "location": loc
    }])
    db.commit()
    print("Book added to DB...\n\n")
    print("...DB Update completed!")


def db_rem_item(isbn):  # method to remove data from multiple call sources
    global db
    global cursor
    print("DB Item Remover started...\n")
    try:
        cursor.execute("DELETE from BOOKS where ISBN=" + isbn)
        print("Book removed Successfully!")
    except:
        print("Book not found! ISBN did not match existing records!")
    db.commit()


def db_export():  # exports entire db contents into a CSV file in root directory
    global cursor
    root = Tk()  # pointing root to Tk() to use it as Tk() in program.
    root.withdraw()  # Hides small tkinter window.
    root.attributes('-topmost', True)  # Opened windows will be active. above all windows despite selection.
    print("Export DB started...")
    data = cursor.execute("SELECT * FROM BOOKS")
    try:
        target_file = filedialog.asksaveasfilename(filetypes=[("csv file", ".csv")], defaultextension=".csv",
                                                   initialfile="books_export")
        with open(target_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([i[0] for i in cursor.description])
            writer.writerows(data)
            print("Data write operation completed!\n\n")
    except Exception as e:
        print("Error - ", e)
        print("\nAborting export operation...\n\n")


def start():  # Also acts as main menu for CLI version
    print("Script started...")
    db_init()
    print("DB init...")

    global db
    global cursor
    print("\033[1;34m"+"\n\n\n"+app_title+"\033[1;m")
    print("\033[1;34m"+random.choice(app_subtitle)+"\033[1;m")

    while True:
        cursor.execute("SELECT * FROM BOOKS")
        db_size = len(cursor.fetchall())
        print("\033[1;35m", "\n\n\n\nDatabase has ", db_size, " books saved.", "\033[1;m")
        print("""
        MENU:
        1 - Book Scanner, Single (ISBN input with Manual input if unmatched)
        2 - Book Scanner, Bulk Load (ISBN input, Copy+Paste from spreadsheet)
        3 - Book Search and Edit (ISBN input)
        4 - View Database
        5 - Export Database (CSV file, Excel compatible)
        6 - Manual Add Mode
        7 - Record Remover
        
        0 - Exit
        
        R - Seek some inspiration
        """)
        sel = input("\nSelection\n> ").lower()
        if sel == "1":
            scanner()
        elif sel == "2":
            scanner()
        elif sel == "3":
            retriever()
        elif sel == "4":
            view_all()
        elif sel == "5":
            db_export()
        elif sel == "6":
            add_isbn = input("What is the ISBN you would like to add?\n> ")
            man_add_mode(add_isbn, False)
        elif sel == "7":
            del_isbn = input("What is the ISBN you would like to remove?\n> ")
            db_rem_item(del_isbn)
        elif sel == "0":
            break
        elif sel == "r":
            print("Enjoy your newfound inspiration!")
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        elif sel == "purge":
            cursor.execute("DROP TABLE BOOKS")
            print("DB Table dropped... Closing app...")
            db.commit()
            break
        else:
            print("Selection not recognised, please choose again!\n")

        # EXPORT NOTES: run 'auto-py-to-exe' within venv to compile standalone program (run 'purge' from menu first!)
        # exporting as onefile does not work at this time...


def db_close_manually():
    db.close()
    print("DB closed...")


if __name__ == "__main__":
    start()
    db_close_manually()
    print("\n"*50)
