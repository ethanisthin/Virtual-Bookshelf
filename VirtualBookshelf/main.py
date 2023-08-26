import re

def isValid(password):
    return len(password) >= 8

def userRegister():
    username = input("For your username, make sure to enter alphanumeric characters and is atleast 5 characters long.\nEnter a username: ")
    while not isValid(username):
        print("Username does not meet the above specified requirements, please try again.")
        username = input("Enter a valid username: ")

    password = input("For your password, make sure it contains alphanumeric characters and is atleast 8 characters long.\nEnter a password: ")
    while not isValid(password):
        print("Password does not meet the above specified requirements, please try again.")
        password = input("Enter a valid password: ")

    with open("user_data.txt", "a") as f:
        f.write(f"Username: {username}, Password: {password}\n")

    print("Registration Successful!")

def compareCredentials(username, password):
    with open('user_data.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            stored_username, stored_password = re.findall(r"Username: (\w+), Password: (\w+)", line)[0]
            if username == stored_username and password == stored_password:
                return True
        return False


def userLogin():
    print("-----Welcome to the Virtual Bookshelf-----")
    userLoginchoice = int(input("If you want to login, enter 1\nIf you want to register, enter 2: "))
    if userLoginchoice == 1:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if compareCredentials(username, password):
            print("Login Sucessful!")
        else:
            print("Invalid username or password.")

    elif userLoginchoice == 2:
        userRegister()

def bookshelfMenu(username):
    print("-----Welcome to the menu, here you can add, view or mark books as completed.-----")
    print("""
          1. Add books 
          2. View books in your bookshelf
          3. Mark books as completed
          4. Exit the bookshelf
          """)
    
    while True:
        userMenuchoice = int(input("Enter the number corresponding to the function you want the program to perform: "))

        if userMenuchoice == 1:
            bookAdd(username)
        if userMenuchoice == 2:
            bookView(username)
        if userMenuchoice == 3:
            markBookCompleted(username)
        if userMenuchoice == 4:
            break

def bookAdd(username):
    print("-----You have chosen to add a book-----")
    print("To get started, enter the title, author, and genre of the book.")
    bookTitle = input("Enter the title of the book: ")
    bookAuthor = input("Enter the name of the author(s): ")
    bookGenre = input("Enter the genre of the book: ")

    with open("user_data.txt", "a") as file:
        file.write(f"Username: {username}, Book: {bookTitle}, Author: {bookAuthor}, Genre: {bookGenre}\n")

    print("Your book has been successfully added!\n")

def bookView(username):
    print("-----Here is your current library-----")
    books = []
    try:
        with open("user_data.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if f"Username: {username}" in line and "Book:" in line:
                    book_title = re.search(r"Book: (.+)", line).group(1)
                    books.append(book_title)

            if not books:
                print("Your bookshelf is empty.\n")
            else:
                for idx, book_title in enumerate(books, start=1):
                    print(f"{idx}. {book_title}")
                
                choice = int(input("Enter the number corresponding to the book you want to mark as completed (0 to cancel): \n"))
                if choice == 0:
                    return
                elif 1 <= choice <= len(books):
                    markBookCompleted(username, books[choice - 1])
                else:
                    print("Invalid choice.")
    except FileNotFoundError:
        print("Your bookshelf is empty.")

def markBookCompleted(username, book_title):
    print("-----You have chosen to mark a book as complete-----")
    books = []
    try:
        with open("user_data.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if f"Username: {username}" in line and "Book:" in line:
                    book_title = re.search(r"Book: (.+)", line).group(1)
                    books.append(book_title)

            if not books:
                print("Your bookshelf is empty.\n")
                return

            for idx, book_title in enumerate(books, start=1):
                print(f"{idx}. {book_title}")
                
            choice = int(input("Enter the number corresponding to the book you want to mark as completed (0 to cancel): \n"))
            if choice == 0:
                return
            elif 1 <= choice <= len(books):
                markBookCompleted(username, books[choice - 1])
            else:
                print("Invalid choice.")
    except FileNotFoundError:
        print("Your bookshelf is empty.")


def userLogin():
    print("-----Welcome to the Virtual Bookshelf-----")
    userLoginchoice = int(input("If you want to login, enter 1\nIf you want to register, enter 2: "))
    if userLoginchoice == 1:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if compareCredentials(username, password):
            print("Login Successful!")
            bookshelfMenu(username)
        else:
            print("Invalid username or password.")

    elif userLoginchoice == 2:
        userRegister()
        userLogin()         

if __name__ == "__main__":
    userLogin()

