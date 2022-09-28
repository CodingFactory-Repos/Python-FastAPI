from fastapi import FastAPI
from routes.index import image

app = FastAPI()

app.include_router(image)
