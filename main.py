############################################
# First Steps
# https://fastapi.tiangolo.com/tutorial/first-steps/
############################################
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

############################################
# Path Parameters
# https://fastapi.tiangolo.com/tutorial/path-params/
############################################


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
