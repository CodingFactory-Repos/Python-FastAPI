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
