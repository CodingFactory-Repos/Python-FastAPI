from sqlalchemy import Table, Column, Integer, String
from config.db import meta

images = Table(
    'images', meta,
    Column('i_id', String(255), primary_key=True),
    Column('i_image', String())
)
