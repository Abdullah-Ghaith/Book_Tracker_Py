import tkinter as tk
import json
from tkinter import messagebox, Listbox, END

#TODO add a delete button
#TODO add a edit button
#TODO add a save button
#TODO add a load button
#TODO add the ability to open a book in a new window, showing all details

class Book:
    def __init__(self, title, author, tags, rating, read_date, description=""):
        self.title = title
        self.author = author
        self.tags = tags
        self.rating = rating
        self.read_date = read_date
        self.description = description

class BookTracker:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_books(self, criteria):
        results = []
        for book in self.books:
            if (criteria in book.title) or (criteria in book.author) or (criteria in book.tags) or (criteria.isdigit() and int(criteria) == book.rating):
                results.append(book)
        return results

    def save_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump([book.__dict__ for book in self.books], file)

    def load_from_json(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.books = [Book(**book_data) for book_data in data]
        except FileNotFoundError:
            pass

class BookTrackerGUI:
    def __init__(self, root):
        self.tracker = BookTracker()
        self.tracker.load_from_json("books.json")  # Load data on startup

        self.root = root
        self.root.title("Book Tracker")

        self.title_label = tk.Label(root, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.author_label = tk.Label(root, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(root)
        self.author_entry.pack()

        self.tags_label = tk.Label(root, text="Tags (comma-separated):")
        self.tags_label.pack()
        self.tags_entry = tk.Entry(root)
        self.tags_entry.pack()

        self.rating_label = tk.Label(root, text="Rating (1-5):")
        self.rating_label.pack()
        self.rating_entry = tk.Entry(root)
        self.rating_entry.pack()

        self.date_label = tk.Label(root, text="Read Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        self.description_label = tk.Label(root, text="Description:")
        self.description_label.pack()
        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
        self.add_button.pack()

        self.search_label = tk.Label(root, text="Search:")
        self.search_label.pack()
        self.search_entry = tk.Entry(root)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Search Books", command=self.search_books)
        self.search_button.pack()

        self.show_all_button = tk.Button(root, text="Show All Books", command=self.show_all_books)
        self.show_all_button.pack()

        self.results_label = tk.Label(root, text="Search Results:")
        self.results_label.pack()
        self.results_listbox = Listbox(root, height=30, width=100)
        self.results_listbox.pack()

        # Create a scrollbar for the listbox
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the scrollbar to work with the listbox
        self.results_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_listbox.yview)

        self.show_all_books()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        tags = [tag.strip() for tag in self.tags_entry.get().split(",")]
        rating = int(self.rating_entry.get())
        read_date = self.date_entry.get()
        description = self.description_entry.get()

        new_book = Book(title, author, tags, rating, read_date, description)
        self.tracker.add_book(new_book)

        messagebox.showinfo("Success", "Book added successfully!")
        self.tracker.save_to_json("books.json")

    def show_all_books(self):
        self.results_listbox.delete(0, END)
        for book in self.tracker.books:
            self.results_listbox.insert(tk.END, f"{book.title} by {book.author}, rating: {book.rating}, read date: {book.read_date}, tags: {book.tags}")

    def search_books(self):
        self.results_listbox.delete(0, END)

        criteria = self.search_entry.get()
        if criteria:
            search_results = self.tracker.search_books(criteria)
            for book in search_results:
                self.results_listbox.insert(tk.END, f"{book.title} by {book.author}, rating: {book.rating}, read date: {book.read_date}, tags: {book.tags}")
        else:
            self.show_all_books()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerGUI(root)
    root.mainloop()
