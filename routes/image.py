import base64

from fastapi import APIRouter, File, UploadFile
from config.db import conn
from models.index import images

image = APIRouter()


@image.get("/{id}")
async def read_image(id: str):
    return conn.execute(images.select().where(images.c.i_id == id)).first()


@image.post("/{id}")
async def create_image(id: str, file: UploadFile):
    # Check if the image already exists
    if conn.execute(images.select().where(images.c.i_id == id)).first():
        return {"status": 400, "message": "ID already used for another image"}
    elif file.content_type.startswith("image/"):
        # Convert image to base64
        image = base64.b64encode(await file.read()).decode("utf-8")

        conn.execute(images.insert().values(i_id=id, i_image=image))

        return {"status": 200, "message": "Image uploaded successfully", "data": conn.execute(images.select().where(images.c.i_id == id)).first()}
    else:
        return {"status": 400, "message": "Invalid image"}


@image.delete("/{id}")
async def delete_image(id: str):
    if conn.execute(images.select().where(images.c.i_id == id)).first():
        conn.execute(images.delete().where(images.c.i_id == id))

        return {"status": 200, "message": "Image deleted successfully"}
    else:
        return {"status": 400, "message": "Image not found"}
