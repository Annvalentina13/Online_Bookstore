# Online Book Store GUI 📘

Welcome to the Online Book Store GUI repository! This desktop application is built using Python's Tkinter and simulates an online bookstore experience. It leverages SQLite as its database backend to manage book details and allows users to browse available books, add items to a shopping cart, and place orders.

## Table of Contents 📑

- [Features 📚](#features-)
- [Prerequisites 🔧](#prerequisites-)
- [Code Overview 🔍](#code-overview-)
  - [Database Setup 🗄](#database-setup-)
  - [Main Application 💻](#main-application-)

## Features 📚

- **Book List Display:**  
  View a list of available books with details such as title, author, price, and stock levels.

- **Add to Cart:**  
  Select a book from the list, enter a desired quantity (with stock verification), and add it to your shopping cart.

- **View Cart:**  
  See the content of your cart including individual subtotals and an overall total.

- **Place Order:**  
  Confirm your purchase, update stock levels in the database, and clear your cart upon successful completion.

- **Exit:**  
  Close the application using the provided exit button.

## Prerequisites 🔧

- **Python 3.x:**  
  Ensure your system has Python 3.6 or above.

- **Tkinter:**  
  Tkinter comes pre-installed with Python; it is used to create the GUI components.

- **SQLite3:**  
  SQLite is used for the database and is included in the Python standard library.

## Code Overview 🔍
   
## Database Setup 🗄
- init_db() Function:

  - Connects to (or creates) an SQLite database file named bookstore_gui.db.
  - Drops the existing books table (if it exists) and creates a fresh one.
  - Defines the table with columns for id, title, author, price, and stock.
  - Inserts a predefined list of books into the table.

- Main Application 💻
  - BookstoreApp Class: This is the main class managing the GUI and the business logic:
  - build_gui() Constructs the main window, title label, listbox (which displays all books), and control buttons (Add to Cart, View Cart, Place Order, and Exit).
  - refresh_books() Retrieves book details from the database and refreshes the listbox with the latest inventory data.
  - add_to_cart() Adds a selected book to the cart after validating the available stock with a prompt for quantity.
  - view_cart() Displays a summary of cart items, including individual prices and the overall total cost.
  - place_order() Processes the order by:
  - Verifying updated stock levels.
  - Deducting the purchased quantities from stock.
  - Clearing the cart after a successful order placement.
