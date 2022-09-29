from sqlalchemy import Table, Column, Integer, String
from config.db import meta

images = Table(
    'images', meta,
    Column('i_fk_user_id', Integer()),
    Column('i_id', String(6), primary_key=True),
    Column('i_image', String())
)
