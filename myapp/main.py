from fastapi import FastAPI, Depends;
from myapp import database
from myapp.database import engine, session

app = FastAPI();

database.Base.metadata.create_all(bind=engine)
def get_db():
    sessionDb = session();
    try:
        yield sessionDb
    finally:
        sessionDb.close();

db_dependency = Depends(get_db)

@app.get("/")
def hello_world():
    return "Hello World";

@app.post("/api/v1/faculty/create")
def create_faculty():
    pass;
