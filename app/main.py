from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, books, reading_list

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reading_list.router)
