import base64

from fastapi import APIRouter, File, UploadFile
from config.db import conn
from models.index import images

image = APIRouter()


@image.get("/")
async def read_images():
    return conn.execute(images.select()).fetchall()


@image.get("/{id}")
async def read_image(id: int):
    return conn.execute(images.select().where(images.c.i_id == id)).first()


@image.post("/{id}")
async def create_image(id: int, file: UploadFile):
    # Check if file is an image
    if file.content_type.startswith("image/"):
        # Convert image to base64
        image = base64.b64encode(await file.read()).decode("utf-8")

        conn.execute(images.insert().values(i_id=id, i_image=image))

        return {"status": 200, "message": "Image uploaded successfully", "data": conn.execute(images.select().where(images.c.i_id == id)).first()}
