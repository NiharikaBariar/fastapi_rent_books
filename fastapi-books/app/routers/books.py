from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.book_model import BookModel, UserModel



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.auth import verify_password, get_password_hash, create_access_token
from ..models.book_model import UserModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
  

@router.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books(database: Session = Depends(get_db)):
    books = database.query(BookModel).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books available.")
    return books

@router.get("/books/{isbn}", response_model=BookModel)
async def get_book_by_isbn(isbn: str, database: Session = Depends(get_db)):
    book = database.query(BookModel).filter(BookModel.ISBN == isbn).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return book

@router.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookModel, database: Session = Depends(get_db)):
    if database.query(BookModel).filter(BookModel.ISBN == book.ISBN).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A book with this ISBN already exists.")
    
    new_book = BookModel(**book.dict())
    database.add(new_book)
    database.commit()
    database.refresh(new_book)
    return new_book

@router.put("/books/{isbn}", response_model=BookModel)
async def update_book(isbn: str, updated_book: BookModel, database: Session = Depends(get_db)):
    book = database.query(BookModel).filter(BookModel.ISBN == isbn).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    
    database.commit()
    database.refresh(book)
    return book

@router.delete("/books/{isbn}")
async def delete_book(isbn: str, database: Session = Depends(get_db)):
    book = database.query(BookModel).filter(BookModel.ISBN == isbn).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    
    database.delete(book)
    database.commit()
    return {"message": "Book deleted successfully"}