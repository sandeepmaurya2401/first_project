from typing import Union

from fastapi import FastAPI, HTTPException
from routers.router_user import router as users_router
import models
import database


app = FastAPI()

app.include_router(users_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/all")
def getAll():
    data = database.getAll()
    return {"data": data}


@app.post("/create")
def create(data:models.Todo):
    id = database.create(data)
    return {"inserted": True, "inserted_id": id}

