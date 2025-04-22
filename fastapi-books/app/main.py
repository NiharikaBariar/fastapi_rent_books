from fastapi import FastAPI
from .routers import books, rentals, user
from .db.database import engine, Base

# Initialize database
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(rentals.router, prefix="/rentals", tags=["Rentals"])
app.include_router(user.router,prefix="/users", tags=["Users"])
# @app.get("/health")
# async def health_check():
#     return {"status": "ok"}
# @app.get("/docs")
# async def docs():
#     return {"message": "API documentation is available at /docs"}
# @app.get("/openapi.json")
# async def openapi():
#     return {"message": "OpenAPI schema is available at /openapi.json"}
# @app.get("/redoc")
# async def redoc():
#     return {"message": "ReDoc documentation is available at /redoc"}
# @app.get("/")
# async def root():
#     return {"message": "Welcome to the FastAPI Books Rental Service!"}