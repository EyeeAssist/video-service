from pydantic import BaseModel


class Video(BaseModel):
    link: str
