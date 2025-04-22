from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BookModel(Base): # Define the SQLAlchemy model
    __tablename__ = "books"  # Define the table name

    id = Column(Integer, primary_key=True, index=True)
    ISBN = Column(String, unique=True, index=True)
    Title = Column(String)
    Author = Column(String)
    YearPublished = Column(Integer)
    CoverImage = Column(String)

class Book(BaseModel): # Define the Pydantic model
    ISBN: str = Field(..., pattern=r"^\d{3}-\d{10}$")  # ISBN-13 format
    Title: str = Field(..., min_length=1, max_length=100)
    Author: str = Field(..., min_length=2, max_length=100)
    YearPublished: int
    CoverImage: str = Field(..., min_length=3, max_length=500)


class RentalModel(Base):
    ISBN: str = Field(..., pattern=r"^\d{3}-\d{10}$")  # ISBN-13 format
    User: str = Field(..., min_length=1, max_length=100)
    RentalDate: datetime
    ReturnDate: datetime = None  # Initially, there is no return date

# Base.metadata.create_all(bind=engine)


