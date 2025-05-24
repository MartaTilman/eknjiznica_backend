from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, books, reviews, ratings, reading_list_user





Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(ratings.router)
app.include_router(reading_list_user.router)
