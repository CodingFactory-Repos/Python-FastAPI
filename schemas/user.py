from pydantic import BaseModel


class User(BaseModel):
    u_id: str
    u_username: str
    u_password: str
    u_email: str
    u_api_key: str
    u_role: str
