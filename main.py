from fastapi import FastAPI
from routes.index import image, user

app = FastAPI()

app.include_router(image)
app.include_router(user)
