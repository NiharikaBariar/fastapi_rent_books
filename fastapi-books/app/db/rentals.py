from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.rental_model import RentalModel
from database import get_db
from datetime import datetime, timedelta

router = APIRouter()

RENTAL_PERIOD_DAYS = 15

@router.post("/rentals", status_code=status.HTTP_201_CREATED)
async def rent_book(isbn: str, user_id: str, db: Session = Depends(get_db)):
    rental_date = datetime.now()
    return_date = rental_date + timedelta(days=RENTAL_PERIOD_DAYS)

    rental = RentalModel(ISBN=isbn, user_id=user_id, rental_date=rental_date, return_date=return_date)
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental

@router.post("/rentals/return", status_code=status.HTTP_200_OK)
async def return_book(isbn: str, user_id: str, db: Session = Depends(get_db)):
    rental = db.query(RentalModel).filter(RentalModel.ISBN == isbn, RentalModel.user_id == user_id).first()
    if not rental:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rental not found.")

    db.delete(rental)
    db.commit()
    return {"message": "Book returned successfully."}

@router.get("/rentals/status/{user_id}", status_code=status.HTTP_200_OK)
async def check_rental_status(user_id: str, db: Session = Depends(get_db)):
    rentals = db.query(RentalModel).filter(RentalModel.user_id == user_id).all()
    if not rentals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No rentals found for this user.")
    return rentals