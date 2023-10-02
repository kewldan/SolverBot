from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    solved: int
    joined: int
