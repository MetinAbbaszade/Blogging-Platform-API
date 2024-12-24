from pydantic import BaseModel
from datetime import datetime
from typing import List

class GetModel(BaseModel):
    id: str | None = None
    title: str
    content: str
    category: str
    tags: List[str]
    created_by: datetime | None = None
    updated_by: datetime | None = None

class PostModel(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]
