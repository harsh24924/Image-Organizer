from typing import List
from pydantic import BaseModel

class Request(BaseModel):
    urls: List[str]

class Image(BaseModel):
    url: str
    caption: str

class Group(BaseModel):
    group_name: str
    images: List[Image]

class Response(BaseModel):
    groups: List[Group]