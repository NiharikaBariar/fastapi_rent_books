# FastAPI Books Rental Application

This project is a FastAPI application that allows users to manage a collection of books and rent them for a maximum period of 15 days. It includes endpoints for book management and rental operations.

## Project Structure

```
fastapi-books
├── app
│   ├── db
│   │   ├── books.py          # Defines data structure and operations related to books
│   │   ├── rentals.py        # Manages rental operations for books
│   │   └── database.py       # Handles database connection and session management
│   ├── models
│   │   ├── book_model.py     # Represents the book entity in the database
│   │   └── rental_model.py    # Represents the rental entity in the database
│   ├── routers
│   │   ├── books.py          # Routes related to book operations
│   │   └── rentals.py        # Routes related to rental operations
│   ├── main.py               # Entry point of the application
│   └── utils
│       └── validators.py     # Utility functions for validating data
├── migrations
│   └── README.md             # Documentation for database migrations
├── requirements.txt          # Lists dependencies required for the project
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-books
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage

- **Book Management:**
  - Retrieve all books: `GET /books`
  - Get a book by ISBN: `GET /books/isbn/{isbn}`
  - Create a new book: `POST /books`
  - Update a book: `PUT /books/{isbn}`
  - Delete a book: `DELETE /books/{isbn}`

- **Rental Operations:**
  - Rent a book: `POST /rentals`
  - Return a book: `DELETE /rentals/{isbn}`
  - Check rental status: `GET /rentals/{isbn}`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

