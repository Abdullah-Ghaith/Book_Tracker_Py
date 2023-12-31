import tkinter as tk
import json
import requests
from tkinter import messagebox, Listbox, END, simpledialog
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO

# CONSTANTS:
NULL_DESCRIPTION = "No description available."

class Book:
    def __init__(self, title, author, tags, rating, read_date, description="", image_link=""):
        self.title = title
        self.author = author
        self.tags = tags
        self.rating = rating
        self.read_date = read_date
        self.description = description
        self.image_link = image_link

class BookTracker:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_books(self, criteria):
        results = []
        for book in self.books:
            if (criteria in book.title) or (criteria in book.author) or (criteria in book.tags) or (
                    criteria.isdigit() and int(criteria) == book.rating):
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
        self.root.geometry("800x800")

        # Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

         # Configure the canvas to work with the scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and the scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


        self.mode = "list"  # Default mode is list view

        self.title_label = tk.Label(self.scrollable_frame, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.scrollable_frame)
        self.title_entry.pack()

        self.author_label = tk.Label(self.scrollable_frame, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(self.scrollable_frame)
        self.author_entry.pack()

        self.tags_label = tk.Label(self.scrollable_frame, text="Tags (comma-separated):")
        self.tags_label.pack()
        self.tags_entry = tk.Entry(self.scrollable_frame)
        self.tags_entry.pack()

        self.rating_label = tk.Label(self.scrollable_frame, text="Rating (1-5):")
        self.rating_label.pack()
        self.rating_entry = tk.Entry(self.scrollable_frame)
        self.rating_entry.pack()

        self.date_label = tk.Label(self.scrollable_frame, text="Read Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.scrollable_frame)
        self.date_entry.pack()

        self.description_label = tk.Label(self.scrollable_frame, text="Description:", wraplength=40)
        self.description_label.pack()
        self.description_entry = tk.Text(self.scrollable_frame, width=50, height=10, wrap="word")
        self.description_entry.pack()

        self.add_button = tk.Button(self.scrollable_frame, text="Add Book", command=self.add_book)
        self.add_button.pack()

        self.scan_button = tk.Button(self.scrollable_frame, text="Scan Book", command=self.prompt_isbn_plus_date)
        self.scan_button.pack()

        self.search_label = tk.Label(self.scrollable_frame, text="Search:")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.scrollable_frame)
        self.search_entry.pack()

        self.search_button = tk.Button(self.scrollable_frame, text="Search Books", command=self.search_books)
        self.search_button.pack()

        # "List View" and "Single View" buttons under "Scan Book"
        self.mode_label = tk.Label(self.scrollable_frame, text="View Mode:")
        self.mode_label.pack()
        self.mode_list_button = tk.Button(self.scrollable_frame, text="List View", command=self.switch_to_list_view)
        self.mode_list_button.pack()
        self.mode_single_button = tk.Button(self.scrollable_frame, text="Single View", command=self.switch_to_single_view)
        self.mode_single_button.pack()
        
        self.show_all_button = tk.Button(self.scrollable_frame, text="Show All Books", command=self.show_all_books)
        self.show_all_button.pack()

        self.remove_button = tk.Button(self.scrollable_frame, text="Remove Book", command=self.remove_book)
        self.remove_button.pack()

        self.results_label = tk.Label(self.scrollable_frame, text="Search Results:")
        self.results_label.pack()
        self.results_listbox = Listbox(self.scrollable_frame, height=30, width=100)
        self.results_listbox.pack()

        # Create a scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.scrollable_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the scrollbar to work with the listbox
        self.results_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_listbox.yview)

        self.show_all_books()

        # Add widgets for single view mode
        self.single_view_frame = tk.Frame(self.scrollable_frame)
        self.image_label = tk.Label(self.single_view_frame)
        self.image_label.pack()

        self.prev_button = tk.Button(self.single_view_frame, text="< Prev", command=self.show_prev_book)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.single_view_frame, text="Next >", command=self.show_next_book)
        self.next_button.pack(side=tk.RIGHT)

        # Use a Text widget for the book label
        self.book_label = tk.Text(self.single_view_frame, wrap="word", width=50, height=10)
        self.book_label.pack()

        # Add a scrollbar to the book label
        self.book_label_scrollbar = tk.Scrollbar(self.single_view_frame, command=self.book_label.yview)
        self.book_label_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.book_label.config(yscrollcommand=self.book_label_scrollbar.set)

        self.current_book_index = 0
        self.show_current_book()

        # Hide the single view frame initially
        self.single_view_frame.pack_forget()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        tags = [tag.strip() for tag in self.tags_entry.get().split(",")]
        rating = int(self.rating_entry.get())
        read_date = self.date_entry.get()
        description = self.description_entry.get('1.0', 'end')

        new_book = Book(title, author, tags, rating, read_date, description)
        self.tracker.add_book(new_book)

        messagebox.showinfo("Success", "Book added successfully!")
        self.tracker.save_to_json("books.json")
        self.show_all_books()

    def _scan_add_book(self, isbn, date_read):
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(url)

        if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    book_data = data['items'][0]['volumeInfo']
                    title = book_data.get('title', '')
                    author = ", ".join(book_data.get('authors', []))
                    tags = book_data.get('categories', [])
                    rating = book_data.get('averageRating', 0)
                    description = book_data.get('description', '')
                    image_link = book_data.get('imageLinks', {}).get('thumbnail', '')

                    # Convert the date to a string representation
                    date_read_str = date_read.isoformat()
                    new_book = Book(title, author, tags, rating, date_read_str, description, image_link)
                    self.tracker.add_book(new_book)
                    self.tracker.save_to_json("books.json")
                    self.show_all_books()
        else:
            print("Error getting book details")
            return None

    def prompt_isbn_plus_date(self):
        user_isbn = simpledialog.askstring("Input", "Enter an ISBN:", parent=self.root)
        if user_isbn is not None:
            user_date_read = simpledialog.askstring("Input", "When did you finish reading this? (YYYY-MM):", parent=self.root, initialvalue=datetime.today().date().strftime("%Y-%m"))
            if user_date_read is not None:
                self._scan_add_book(isbn=user_isbn, date_read=datetime.strptime(user_date_read, "%Y-%m").date())
            else:
                messagebox.showerror("Error", "No date entered!")

    def show_all_books(self):
        self.results_listbox.delete(0, END)
        for book in self.tracker.books:
            self.results_listbox.insert(tk.END,
                                        f"{book.title} by {book.author}, rating: {book.rating}, read date: {book.read_date}, tags: {book.tags}")

    def search_books(self):
        self.results_listbox.delete(0, END)

        criteria = self.search_entry.get()
        if criteria:
            search_results = self.tracker.search_books(criteria)
            for book in search_results:
                self.results_listbox.insert(tk.END,
                                            f"{book.title} by {book.author}, rating: {book.rating}, read date: {book.read_date}, tags: {book.tags}")
        else:
            self.show_all_books()

    def remove_book(self):
        selected_book = self.results_listbox.get(self.results_listbox.curselection())
        if selected_book:
            book_title = selected_book.split(" by ")[0]
            for book in self.tracker.books:
                if book.title == book_title:
                    self.tracker.books.remove(book)
                    messagebox.showinfo("Success", "Book removed successfully!")
                    self.tracker.save_to_json("books.json")
                    self.show_all_books()
                    break
        else:
            messagebox.showerror("Error", "No book selected!")

    def switch_to_list_view(self):
        self.mode = "list"
        self.mode_list_button.config(state=tk.DISABLED)
        self.mode_single_button.config(state=tk.NORMAL)
        self.results_listbox.pack()
        self.single_view_frame.pack_forget()

    def switch_to_single_view(self):
        self.mode = "single"
        self.mode_single_button.config(state=tk.DISABLED)
        self.mode_list_button.config(state=tk.NORMAL)
        self.results_listbox.pack_forget()
        self.single_view_frame.pack(side=tk.TOP)

        # Show the current book in single view
        self.show_current_book()

    def show_current_book(self):
        if len(self.tracker.books) > 0:
                book = self.tracker.books[self.current_book_index]
                # Make sure the Text widget is in 'normal' state before updating the text
                self.book_label.config(state='normal')
                self.book_label.delete('1.0', 'end')
                self.book_label.insert('1.0', f"{book.title} by {book.author}, rating: {book.rating}, read date: {book.read_date}, tags: {book.tags}, description: {book.description}")
                self.book_label.config(state='disabled')  # Make the Text widget read-only

                # Load and display the image
                if book.image_link:  # Check if the image link is not empty
                    response = requests.get(book.image_link)
                    img_data = response.content
                    img = Image.open(BytesIO(img_data))
                    img = img.resize((160, 160), Image.BICUBIC)  # Resize the image
                    img = ImageTk.PhotoImage(img)
                    self.image_label.config(image=img)
                    self.image_label.image = img  # Keep a reference to the image
        else:
            self.book_label.config(state='normal')
            self.book_label.delete('1.0', 'end')
            self.book_label.insert('1.0', "No books found")
            self.book_label.config(state='disabled')

    def show_prev_book(self):
        if self.current_book_index > 0:
            self.current_book_index -= 1
            self.show_current_book()

    def show_next_book(self):
        if self.current_book_index < len(self.tracker.books) - 1:
            self.current_book_index += 1
            self.show_current_book()

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerGUI(root)
    root.mainloop()