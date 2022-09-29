import base64
import os

from fastapi import APIRouter, File, UploadFile

from config.db import conn
from models.index import users

user = APIRouter()
prefix = "/user"


@user.post(prefix + "/register")
async def register_user(username: str, password: str, email: str):
    """
    It registers a user.

    :param username: The username of the user
    :type username: str
    :param password: The password of the user
    :type password: str
    :param email: The email of the user
    :type email: str
    :return: A dictionary with the status, message and data.
    """

    ##############
    # Conditions #
    ##############
    # Check if the user exists
    if conn.execute(users.select().where(users.c.u_username == username)).first():
        return {"status": 400, "message": "Username already used for another user"}

    if conn.execute(users.select().where(users.c.u_email == email)).first():
        return {"status": 400, "message": "Email already used for another user"}
    #####################
    # End of conditions #
    #####################

    # Generating a random string of 24 characters and encoding it in base64.
    api_key = base64.b64encode(os.urandom(24)).decode("utf-8")
    # Inserting the values into the database.
    conn.execute(users.insert().values(u_username=username, u_password=password, u_email=email, u_api_key=api_key))
    return {"status": 200, "message": "User created successfully", "data": {"username": username, "email": email, "api_key": api_key}}


@user.post(prefix + "/login")
async def login_user(username: str, password: str):
    """
    It checks if the user exists, if the password is correct and if it is, it returns a token.

    :param username: The username of the user
    :type username: str
    :param password: The password of the user
    :type password: str
    :return: A dictionary with the status, message and token.
    """
    
    ##############
    # Conditions #
    ##############
    # Check if the user exists
    if not conn.execute(users.select().where(users.c.u_username == username)).first():
        return {"status": 400, "message": "Username not found"}

    user = conn.execute(users.select().where(users.c.u_username == username)).first()

    # Check if the password is correct
    if not user["u_password"] == password:
        return {"status": 400, "message": "Incorrect password"}
    #####################
    # End of conditions #
    #####################

    # Returning a dictionary with the status, message and token.
    return {"status": 200, "message": "User logged in successfully", "token": user['u_api_key']}
