from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db.database import Base

class UserModel(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


