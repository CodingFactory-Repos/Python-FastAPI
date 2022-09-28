import base64

from fastapi import APIRouter, File, UploadFile
from config.db import conn
from models.index import images

image = APIRouter()


@image.get("/")
async def read_images():
    return conn.execute(images.select()).fetchall()
