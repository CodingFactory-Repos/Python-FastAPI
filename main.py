from fastapi import FastAPI
import User

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

user = User.User("Michel")

print(User.get_person_name(user))
