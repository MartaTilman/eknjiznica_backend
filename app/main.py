from fastapi import FastAPI
import socket,os
from app.database import engine, Base
from app.models import book, user
app = FastAPI()

@app.get("/")
def read_root():
    hostname = socket.gethostname()
    port = os.getenv("PORT", "unknown")
    return {"message": f"Pozdrav s instance: {hostname}, port: {port}"}
@app.get("/")
def root():
    return {"message": "eKnjižnica backend radi"}
