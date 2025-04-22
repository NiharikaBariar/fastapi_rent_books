from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgresql_database_url = "postgresql://postgres:pg12345@localhost/books_db"
engine = create_engine(postgresql_database_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

