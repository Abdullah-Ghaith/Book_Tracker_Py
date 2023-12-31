# Book Tracker

This is a simple book tracking application written in Python. It uses a GUI built with Tkinter and can save and load book data to and from a JSON file.

## Requirements

- Python 3
- Tkinter
- PIL
- requests

## How to Run

1. Ensure you have Python 3 installed on your machine.
2. Install the required Python packages if you haven't already. You can do this by running `pip install tkinter PIL requests`.
3. Run `main.py` with Python 3. You can do this by running `python3 main.py` in your terminal.

## How to Use

The application has a GUI that allows you to interact with it.

- To add a book manually, fill in the fields in the GUI and click the "Add Book" button.
- To add a book by scanning its ISBN, click the "Scan ISBN" button and follow the prompts.
- To view all books, click the "Show All Books" button.
- To search for a book, enter your search query in the search field and click the "Search" button.
- To remove a book, select it from the list and click the "Remove Book" button.

The application will automatically save your book data to a JSON file named `books.json` whenever you add or remove a book.