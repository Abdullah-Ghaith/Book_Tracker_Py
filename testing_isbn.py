import requests
from IPython.display import Image, display


def get_book_details(isbn):
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

            if image_link:
                display(Image(url=image_link))

            return {
                'title': title,
                'author': author,
                'tags': tags,
                'rating': rating,
                'description': description,
            }
        else:
            return None
    else:
        return None
    
if __name__ == "__main__":
    print(get_book_details("9780393325348"))