import re
import sqlite3

#*Checking if password length is 8 characters or above
def isValid(password):
    return len(password) >= 8



#*Creates database tables to store user credentials/book data
def create_tables():
    conn = sqlite3.connect("bookshelf.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            author TEXT,
            genre TEXT,
            completed INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    conn.commit()
    conn.close()



#*Compares credentials with database entries
def compareCredentials(username, password):
    conn = sqlite3.connect("bookshelf.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password FROM users WHERE username = ?", (username,)
    )
    result = cursor.fetchone()

    conn.close()

    if result and result[1] == password:
        return True
    return False



#*Registers a new user into the database and checks username/password requirements
def userRegister():
    username = input(
        "For your username, make sure to enter alphanumeric characters and is at least 5 characters long.\nEnter a username: "
    )
    while not isValid(username):
        print(
            "Username does not meet the above specified requirements, please try again."
        )
        username = input("Enter a valid username: ")

    password = input(
        "For your password, make sure it contains alphanumeric characters and is at least 8 characters long.\nEnter a password: "
    )
    while not isValid(password):
        print(
            "Password does not meet the above specified requirements, please try again."
        )
        password = input("Enter a valid password: ")

    conn = sqlite3.connect("bookshelf.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )

    conn.commit()
    conn.close()

    print("Registration Successful!")



#*Adds a book to the database
def bookAdd(user_id):
    print("-----You have chosen to add a book-----")
    print("To get started, enter the title, author, and genre of the book.")
    bookTitle = input("Enter the title of the book: ")
    bookAuthor = input("Enter the name of the author(s): ")
    bookGenre = input("Enter the genre of the book: ")

    conn = sqlite3.connect("bookshelf.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (user_id, title, author, genre, completed) VALUES (?, ?, ?, ?, ?)",
        (user_id, bookTitle, bookAuthor, bookGenre, False),
    )

    conn.commit()
    conn.close()

    print("Your book has been successfully added!\n")



#*Allows user to view books in their bookshelf
def bookView(user_id):
    print("-----Here is your current library-----")
    conn = sqlite3.connect("bookshelf.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, author, completed FROM books WHERE user_id = ?", (user_id,))
    books = cursor.fetchall()

    conn.close()

    if not books:
        print("Your bookshelf is empty.\n")
    else:
        for index, (bookTitle, bookAuthor, completed) in enumerate(books, start=1):
            completeStatus = "Yes" if completed == 1 else "No"
            print(f"{index}. {bookTitle} | {bookAuthor} | {completeStatus} \n")

        choice = int(
            input(
                "Enter the number corresponding to the book you want to mark as completed (0 to cancel): \n"
            )
        )
        if choice == 0:
            return
        elif 1 <= choice <= len(books):
            markBookCompleted(user_id, books[choice - 1][0])
        else:
            print("Invalid choice.")



#*Allows the user to mark a book as completed
def markBookCompleted(user_id, book_title):
    print("-----You have chosen to mark a book as complete-----")
    conn = sqlite3.connect("bookshelf.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE books SET completed = ? WHERE user_id = ? AND title = ?", (1, user_id, book_title))
    conn.commit()

    conn.close()

    print(f"The book '{book_title}' has been marked as completed.\n")



#*Allows a user to login to an existing account
def userLogin():
    print("-----Welcome to the Virtual Bookshelf-----")
    userLoginchoice = int(
        input("If you want to login, enter 1\nIf you want to register, enter 2: ")
    )

    conn = sqlite3.connect("bookshelf.db")
    cursor = conn.cursor()

    if userLoginchoice == 1:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        result = cursor.fetchone()

        if result:
            print("Login Successful!")
            bookshelfMenu(result[0])
        else:
            print("Invalid username or password.")

    elif userLoginchoice == 2:
        userRegister()
        userLogin()

    conn.close()



#*Displays a menu in which the user can choose which function for the program to perform
def bookshelfMenu(user_id):
    print(
        "-----Welcome to the menu, here you can add, view or mark books as completed.-----"
    )
    print(
        """
          1. Add books 
          2. View books in your bookshelf
          3. Mark books as completed
          4. Exit the bookshelf
          """
    )

    while True:
        userMenuchoice = int(
            input(
                "Enter the number corresponding to the function you want the program to perform: "
            )
        )

        if userMenuchoice == 1:
            bookAdd(user_id)
        if userMenuchoice == 2:
            bookView(user_id)
        if userMenuchoice == 3:
            bookView(user_id)
        if userMenuchoice == 4:
            break


if __name__ == "__main__":
    create_tables()
    userLogin()
