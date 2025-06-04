import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# ------------------- DATABASE SETUP -------------------
def init_db():
    conn = sqlite3.connect('bookstore_gui.db')
    cur = conn.cursor()
    
    # Drop existing table to start fresh
    cur.execute("DROP TABLE IF EXISTS books")
    
    cur.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )''')

    books = [
        ("The Alchemist", "Paulo Coelho", 299, 10),
        ("Wings of Fire", "A.P.J Abdul Kalam", 199, 8),
        ("1984", "George Orwell", 249, 5),
        ("Clean Code", "Robert Martin", 550, 3),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 399, 15),
        ("The Da Vinci Code", "Dan Brown", 349, 7),
        ("To Kill a Mockingbird", "Harper Lee", 279, 6),
        ("The Lord of the Rings", "J.R.R. Tolkien", 599, 4),
        ("Pride and Prejudice", "Jane Austen", 199, 12),
        ("The Hobbit", "J.R.R. Tolkien", 349, 9),
        ("The Silent Patient", "Alex Michaelides", 399, 8),
        ("Atomic Habits", "James Clear", 449, 10),
        ("The Psychology of Money", "Morgan Housel", 299, 7),
        ("Sapiens", "Yuval Noah Harari", 499, 6),
        ("The Midnight Library", "Matt Haig", 349, 9),
        ("Rich Dad Poor Dad", "Robert Kiyosaki", 299, 12),
        ("Think and Grow Rich", "Napoleon Hill", 249, 8),
        ("The Great Gatsby", "F. Scott Fitzgerald", 199, 11),
        ("Animal Farm", "George Orwell", 249, 7),
        ("The Power of Now", "Eckhart Tolle", 299, 5),
        ("Dune", "Frank Herbert", 449, 6),
        ("The Catcher in the Rye", "J.D. Salinger", 279, 8),
        ("The Kite Runner", "Khaled Hosseini", 349, 7),
        ("Life's Amazing Secrets", "Gaur Gopal Das", 249, 10),
        ("Norwegian Wood", "Haruki Murakami", 399, 5)
    ]
    
    # Insert all books directly without checking
    cur.executemany("INSERT INTO books (title, author, price, stock) VALUES (?, ?, ?, ?)", books)
    conn.commit()
    conn.close()
# ------------------- MAIN APPLICATION -------------------
class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Book Store")
        self.cart = []
        self.build_gui()

    def build_gui(self):
        # Make the window size more reasonable
        self.root.geometry("800x400")
        
        # Add a title label
        title_label = tk.Label(self.root, text="Welcome to Online Book Store", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)

        self.book_listbox = tk.Listbox(self.root, width=80, height=15)
        self.book_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.refresh_books()

        # Add some padding and make buttons wider
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(button_frame, text="Add to Cart", width=15, command=self.add_to_cart).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="View Cart", width=15, command=self.view_cart).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Place Order", width=15, command=self.place_order).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exit", width=15, command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def refresh_books(self):
        try:
            self.book_listbox.delete(0, tk.END)
            conn = sqlite3.connect('bookstore_gui.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM books")
            books = cur.fetchall()
            for book in books:
                line = f"{book[0]}: {book[1]} by {book[2]} - ₹{book[3]} (Stock: {book[4]})"
                self.book_listbox.insert(tk.END, line)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def add_to_cart(self):
        try:
            selection = self.book_listbox.get(self.book_listbox.curselection())
            book_id = int(selection.split(":")[0])
            qty = simpledialog.askinteger("Quantity", "Enter quantity:", minvalue=1)
            if qty is not None:
                # Check stock before adding to cart
                conn = sqlite3.connect('bookstore_gui.db')
                cur = conn.cursor()
                cur.execute("SELECT stock, title FROM books WHERE id=?", (book_id,))
                stock, title = cur.fetchone()
                if qty > stock:
                    messagebox.showwarning("Stock Issue", f"Not enough stock. Only {stock} copies available.")
                    conn.close()
                    return
                self.cart.append((book_id, qty))
                messagebox.showinfo("Added", f"Added {qty} copies of '{title}' to cart.")
                conn.close()
        except tk.TclError:
            messagebox.showwarning("Error", "Please select a book first.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def view_cart(self):
        if not self.cart:
            messagebox.showinfo("Cart", "Cart is empty.")
            return

        try:
            conn = sqlite3.connect('bookstore_gui.db')
            cur = conn.cursor()
            cart_details = "Your Cart:\n\n"
            total = 0
            for book_id, qty in self.cart:
                cur.execute("SELECT title, price FROM books WHERE id=?", (book_id,))
                title, price = cur.fetchone()
                subtotal = price * qty
                total += subtotal
                cart_details += f"{title} x {qty} = ₹{subtotal}\n"
            conn.close()

            cart_details += f"\nTotal: ₹{total}"
            messagebox.showinfo("Cart Items", cart_details)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

    def place_order(self):
        if not self.cart:
            messagebox.showwarning("Empty", "Cart is empty.")
            return

        try:
            conn = sqlite3.connect('bookstore_gui.db')
            cur = conn.cursor()
            
            # Check stock availability
            for book_id, qty in self.cart:
                cur.execute("SELECT title, stock FROM books WHERE id=?", (book_id,))
                title, stock = cur.fetchone()
                if stock < qty:
                    messagebox.showwarning("Stock Issue", f"Not enough stock for '{title}'.")
                    conn.close()
                    return

            # Update stock
            for book_id, qty in self.cart:
                cur.execute("UPDATE books SET stock = stock - ? WHERE id = ?", (qty, book_id))
            
            conn.commit()
            conn.close()
            self.cart.clear()
            self.refresh_books()
            messagebox.showinfo("Success", "Order placed successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()