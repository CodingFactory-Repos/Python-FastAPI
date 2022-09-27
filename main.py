from fastapi import FastAPI
import User

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

new_user = User.User("Michel", 47, "18 janvier 1975", 10)

User.get_user_infos(new_user)
