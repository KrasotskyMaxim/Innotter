from fastapi import FastAPI
from utils import init_db


db = init_db()
app = FastAPI() 


@app.get("/")
def read_root():
    return {"Hello": "World"} 
