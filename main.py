from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


people = [
    {"id": 1, "first_name": "Ali", "last_name": "Ahmadi", "age": 25, "gender": "M"},
    {"id": 2, "first_name": "Sara", "last_name": "Hosseini", "age": 30, "gender": "F"},
    {"id": 3, "first_name": "Reza", "last_name": "Karimi", "age": 28, "gender": "M"},
    {"id": 4, "first_name": "Fatemeh",
        "last_name": "Najafi", "age": 27, "gender": "F"},
    {"id": 5, "first_name": "Mohammad",
        "last_name": "Rezaei", "age": 32, "gender": "M"},
    {"id": 6, "first_name": "Zahra", "last_name": "Ghasemi", "age": 26, "gender": "F"},
    {"id": 7, "first_name": "Hossein",
        "last_name": "Rahimi", "age": 29, "gender": "M"},
    {"id": 8, "first_name": "Narges", "last_name": "Jafari", "age": 24, "gender": "F"},
    {"id": 9, "first_name": "Ahmad", "last_name": "Pouri", "age": 31, "gender": "M"},
    {"id": 10, "first_name": "Leyla", "last_name": "Fazeli", "age": 23, "gender": "F"},
]

class Person(BaseModel):
    id: int


@app.post("/person/")
async def get_person(prs: Person):
    find_person = {p["id"]:p for p in people}[prs.id]
    return find_person
