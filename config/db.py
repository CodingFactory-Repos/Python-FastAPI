from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:root@localhost:8889/python-image-api")

meta = MetaData()
conn = engine.connect()
