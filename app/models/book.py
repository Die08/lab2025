from pydantic import BaseModel, Field
from typing import Annotated


class Book(BaseModel):
    id: int
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)] = None
