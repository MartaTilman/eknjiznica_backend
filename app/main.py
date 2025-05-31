from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, books, reviews, ratings, reading_list_user, wish_list
from app import models
import os
import uvicorn
from fastapi.responses import RedirectResponse



Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(ratings.router)
app.include_router(reading_list_user.router)
app.include_router(wish_list.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)