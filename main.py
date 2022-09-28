import json

from fastapi import FastAPI
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_images_db = [{"image_name": "/images/sun-ken-rock.png"}, {"item_name": "ranjdqlf"}]


app = FastAPI()


@app.get("/images/")
async def get_image(skip: int = 3, limit: int = 10):
    return fake_images_db[skip: skip + limit]


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model.name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"RICK", "Morty"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
