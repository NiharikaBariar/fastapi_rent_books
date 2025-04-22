# This is a Python script that defines a list of movies and a Movie class to represent each movie.
from fastapi import FastAPI, Path, Query, Depends, status, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime as now

app = FastAPI()

Books=[
  {
    "ISBN": "9780321765723",
    "Title": "The Lord of the Rings",
    "Author": "J.R.R. Tolkien",
    "YearOfPublish": 1954,
    "CoverImage": "https://example.com/covers/lord_of_the_rings.jpg"
  },
  {
    "ISBN": "9780743273565",
    "Title": "The Great Gatsby",
    "Author": "F. Scott Fitzgerald",
    "YearOfPublish": 1925,
    "CoverImage": "https://example.com/covers/great_gatsby.jpg"
  },
  {
    "ISBN": "9780061120084",
    "Title": "To Kill a Mockingbird",
    "Author": "Harper Lee",
    "YearOfPublish": 1960,
    "CoverImage": "https://example.com/covers/to_kill_a_mockingbird.jpg"
  },
  {
    "ISBN": "9780743297448",
    "Title": "The Hitchhiker's Guide to the Galaxy",
    "Author": "Douglas Adams",
    "YearOfPublish": 1979,
    "CoverImage": "https://example.com/covers/hitchhikers_guide.jpg"
  },
  {
    "ISBN": "9780553807886",
    "Title": "A Game of Thrones",
    "Author": "George R.R. Martin",
    "YearOfPublish": 1996,
    "CoverImage": "https://example.com/covers/game_of_thrones.jpg"
  }
]

class Book(BaseModel):
    ISBN: str = Field(..., pattern=r"^\d{3}-\d{10}$") # ISBN-13 format
    Title: str = Field(min_length=1, max_length=100)
    Author: str = Field(min_length=2, max_length=100)
    YearOfPublish: int 
    CoverImage: str = Field(min_length=3, max_length=500)

    @field_validator('YearOfPublish')
    def validate_year(cls, y):
        current_year = now.now().year
        if y > current_year:
            raise ValueError('Year of publish must not be greater than the', f'current year {current_year}')
        return y
    

@app.get("/books", status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_all_books():
    ''' Returns 200 OK '''
    if not Books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No books available."
        )
    return Books


@app.get("/books/isbn/{isbn}/", status_code=status.HTTP_200_OK, response_model=Book)
async def get_book_by_isbn(isbn: str = Path(..., regex=r"^\d{3}-\d{10}$")):
    ''' This loop iterates over the books object, which contains all books. '''
    for book in Books:
        if book.ISBN == isbn:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found with this ISBN."
    )

@app.get("/books/author", status_code=status.HTTP_200_OK)
async def get_books_by_author(author: str = Query(..., min_length=2, max_length=100)):
    ''' 
    This line creates a list comprehension to filter books from the books object based on whether 
    the Author attribute matches the specified author.
    '''
    books_by_author = [book for book in Books if book.Author == author]
    if not books_by_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No books found for this author."
        )
    '''This returns the list books_by_author'''
    return books_by_author

@app.put("/books/{isbn}", status_code=status.HTTP_200_OK)
async def update_book(book: Book, isbn: str = Path(..., regex=r"^\d{3}-\d{10}$")):
    ''' This loop iterates over the books object, which contains all books. '''
    for index, book in enumerate(Books):
        if book.ISBN == isbn:
            Books[index] = book.model_dump()
            return {"message": "Book updated successfully","book": book}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
    )

@app.delete("/books/{isbn}", status_code=status.HTTP_200_OK)
async def delete_book(isbn: str = Path(..., regex=r"^\d{3}-\d{10}$")):
    ''' This loop iterates over the books object, which contains all books. '''
    for index, book in enumerate(Books):
        if book["ISBN"] == isbn:
            Books.pop(index)
            return {"message": "Book deleted successfully"}
    # If no book with the provided ISBN is found during the loop Raises an HTTP exception
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found with ISBN {isbn}."
    )


@app.post(status_code=status.HTTP_201_CREATED) # 201 Created on successful creation
async def create_book(book: Book):
    ''' Exception
    any() checks the condition (existing_book.ISBN == book.ISBN) for each existing_book in the books_db.
    If a match is found, it immediately returns True and raises the HTTPException.
    '''
    if any(existing_book.ISBN == book.ISBN for existing_book in Books):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="A book with this ISBN already exists."
        )

    Books.append(book)
    return book