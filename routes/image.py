import base64
from enum import Enum

import cv2
import numpy as np

from fastapi import APIRouter, File, UploadFile
from config.db import conn
from models.index import images
from models.index import users

image = APIRouter()
prefix = "/image"


@image.get(prefix)
async def get_all_images(token: str):
    """
    It's getting all the images from the database and returning them.

    :param token: The token of the user
    :type token: str
    :return: It's returning a list of dictionaries, each dictionary contains the id and the image of the image.
    """

    # It's getting the user from the database.
    user = conn.execute(users.select().where(users.c.u_api_key == token)).first()

    ##############
    # Conditions #
    ##############
    # Check if the user exists
    if not user:
        return {"status": 400, "message": "Invalid token"}

    # Check if the user has images
    if not conn.execute(images.select().where(images.c.i_fk_user_id == user["u_id"])).first():
        return {"status": 400, "message": "No images found"}
    #####################
    # End of conditions #
    #####################

    # It's getting all the images from the database and returning them.
    images_list = []
    for image in conn.execute(images.select().where(
            images.c.i_fk_user_id == conn.execute(users.select().where(users.c.u_api_key == token)).first()["u_id"])):
        images_list.append({"id": image["i_id"], "image": image["i_image"]})

    return {"status": 200, "message": "Images found", "data": images_list}


@image.get(prefix + "/{id}")
async def read_image(id: str, token: str):
    """
    It's getting the image from the database and returning it.

    :param id: The id of the image
    :type id: str
    :param token: The token of the user
    :type token: str
    :return: The image is being returned.
    """

    # It's getting the user from the database.
    user = conn.execute(users.select().where(users.c.u_api_key == token)).first()

    ##############
    # Conditions #
    ##############
    # It's checking if the user is valid.
    if not user:
        return {"status": 400, "message": "Invalid token"}

    # It's checking if the image exists.
    if not conn.execute(images.select().where(images.c.i_id == id)).first():
        return {"status": 400, "message": "Image not found"}

    # It's checking if the user has access to the image.
    if not conn.execute(
            images.select().where(images.c.i_id == id).where(images.c.i_fk_user_id == user["u_id"])).first() and user["u_role"] != "admin":
        return {"status": 400, "message": "You don't have access to this image"}
    #####################
    # End of conditions #
    #####################

    # It's getting the image from the database and returning it.
    image = conn.execute(images.select().where(images.c.i_id == id)).first()
    return {"status": 200, "message": "Image found", "data": {"id": image['i_id'], "image": image['i_image']}}


@image.post(prefix + "/{id}")
async def create_image(id: str, file: UploadFile, token: str):
    """
    It's getting the user from the database, checking if the user is valid, checking if the image already exists, checking
    if the file is an image, converting the image to base64 and then inserting it into the database

    :param id: The ID of the image
    :type id: str
    :param file: UploadFile - It's the file that the user is uploading
    :type file: UploadFile
    :param token: The token of the user
    :type token: str
    :return: It's returning the image that was just uploaded.
    """

    # It's getting the user from the database.
    user = conn.execute(users.select().where(users.c.u_api_key == token)).first()

    ##############
    # Conditions #
    ##############
    # Checking if the user is valid.
    if not user:
        return {"status": 400, "message": "Invalid token"}

    # Checking if the image already exists.
    if conn.execute(images.select().where(images.c.i_id == id)).first():
        return {"status": 400, "message": "ID already used for another image"}

    # It's checking if the file is an image.
    if not file.content_type.startswith("image/"):
        return {"status": 400, "message": "Invalid image"}

    # Check if the user have already uploaded 5 images.
    if len(conn.execute(images.select().where(images.c.i_fk_user_id == user["u_id"])).fetchall()) >= 5 and user["u_role"] != "admin":
        return {"status": 400,
                "message": "You can't upload more than 5 images, please delete one of your images and try again"}
    #####################
    # End of conditions #
    #####################

    # It's converting the image to base64 and then inserting it into the database.
    image = base64.b64encode(await file.read()).decode("utf-8")

    conn.execute(images.insert().values(i_id=id, i_image=image, i_fk_user_id=user['u_id']))

    return {"status": 200, "message": "Image uploaded successfully",
            "data": conn.execute(images.select().where(images.c.i_id == id)).first()}


@image.delete(prefix + "/{id}")
async def delete_image(id: str, token: str):
    """
    It's deleting an image from the database.

    :param id: The id of the image
    :type id: str
    :param token: The user's token
    :type token: str
    :return: It's returning the status of the request and a message.
    """

    # It's getting the user from the database.
    user = conn.execute(users.select().where(users.c.u_api_key == token)).first()

    ##############
    # Conditions #
    ##############
    # It's checking if the user is valid.
    if not user:
        return {"status": 400, "message": "Invalid token"}

    # It's checking if the image exists.
    if not conn.execute(images.select().where(images.c.i_id == id)).first():
        return {"status": 400, "message": "Image not found"}

    # It's checking if the user has access to the image.
    if not conn.execute(
            images.select().where(images.c.i_id == id).where(images.c.i_fk_user_id == user["u_id"])).first() and user["u_role"] != "admin":
        return {"status": 400, "message": "You don't have access to this image"}
    #####################
    # End of conditions #
    #####################

    # It's deleting the image from the database.
    conn.execute(images.delete().where(images.c.i_id == id))
    return {"status": 200, "message": "Image deleted successfully"}


class Filters(str, Enum):
    """
    It's the filters that the user can use
    """
    grayscale = "grayscale"
    invert = "invert"
    blur = "blur"
    contour = "contour"
    emboss = "emboss"


@image.put(prefix + "/{id}")
async def add_filter_image(id: str, token: str, filter: Filters):
    """
    It's getting the user from the database, checking if the user is valid, checking if the image exists, checking if the
    user has access to the image, checking if the filter is valid, checking if the filter is already applied, applying the
    filter and then updating the image in the database.

    :param id: The id of the image
    :type id: str
    :param token: The user's token
    :type token: str
    :param filters: The filter that the user wants to apply
    :type filters: Filter
    :return: It's returning the status of the request and a message.
    """

    # It's getting the user from the database.
    user = conn.execute(users.select().where(users.c.u_api_key == token)).first()

    ##############
    # Conditions #
    ##############
    # It's checking if the user is valid.
    if not user:
        return {"status": 400, "message": "Invalid token"}

    # It's checking if the image exists.
    if not conn.execute(images.select().where(images.c.i_id == id)).first():
        return {"status": 400, "message": "Image not found"}

    # It's checking if the user has access to the image.
    if not conn.execute(
            images.select().where(images.c.i_id == id).where(images.c.i_fk_user_id == user["u_id"])).first() and user["u_role"] != "admin":
        return {"status": 400, "message": "You don't have access to this image"}

    # It's checking if the filter is valid.
    if filter not in Filters:
        return {"status": 400, "message": "Invalid filter", "allFilters": [f.value for f in Filters]}
    #####################
    # End of conditions #
    #####################

    # It's applying the filter with CV2.
    image = conn.execute(images.select().where(images.c.i_id == id)).first()
    image = base64.b64decode(image["i_image"])
    nparr = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # It's applying the filter to the image.
    if filter == Filters.grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif filter == Filters.invert:
        img = cv2.bitwise_not(img)
    elif filter == Filters.blur:
        img = cv2.blur(img, (5, 5))
    elif filter == Filters.contour:
        img = cv2.Canny(img, 100, 200)
    elif filter == Filters.emboss:
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])
        img = cv2.filter2D(img, -1, kernel)

    # It's converting the image to base64.
    _, buffer = cv2.imencode('.jpg', img)
    img = base64.b64encode(buffer)

    # It's updating the image in the database.
    conn.execute(images.update().where(images.c.i_id == id).values(i_image=img))
    return {"status": 200, "message": "Filter applied successfully", "data": conn.execute(images.select().where(images.c.i_id == id)).first()}
