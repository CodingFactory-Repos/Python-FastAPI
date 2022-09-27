from fastapi import FastAPI
import User

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

new_user = User.User("Michel", 47, "18 january 1975", 10)

User.get_user_infos(new_user)
