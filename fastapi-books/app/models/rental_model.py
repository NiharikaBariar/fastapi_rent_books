from pydantic import BaseModel
from datetime import datetime

class RentalModel(BaseModel):
    ISBN: str
    user_id: str
    rental_date: datetime
    return_date: datetime

    class Config:
        orm_mode = True