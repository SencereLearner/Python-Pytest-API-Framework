from pydantic import BaseModel

class PostResponseModel(BaseModel):
    id: int
    title: str
    body: str
    userId: int
