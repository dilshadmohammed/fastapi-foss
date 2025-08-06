from fastapi import FastAPI
from fastapi import Query

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Welcome to the Quiz API!"}

@app.get("/welcome")
def welcome(name: str = "No name"):
    return {"message": f"Welcome to the Quiz API, {name}!"}
