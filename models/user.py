from sqlalchemy import Table, Column, Integer, String
from config.db import meta

users = Table(
    'users', meta,
    Column('u_id', Integer(), primary_key=True, autoincrement=True),
    Column('u_username', String(20), unique=True),
    Column('u_password', String(100)),
    Column('u_email', String(50), unique=True),
    Column('u_api_key', String(32), unique=True),
    Column('u_role', String(10))
)
