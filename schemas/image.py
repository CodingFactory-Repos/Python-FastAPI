from pydantic import BaseModel


class Image(BaseModel):
    i_id: str
    i_image: str
