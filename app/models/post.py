from sqlmodel import Field
from typing import Optional, List
from app.models.basemodel import BaseClass


class Post(BaseClass, table=True):
    title: str = Field(max_length=100)
    content: str
    category: str
    tags: Optional[str] = Field(default=None)

    def to_dict(self) -> dict:
        dictionary = super().to_dict()
        tags_list = self.tags.split(',') if self.tags else []
        dictionary.update({
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": tags_list,
        })
        return dictionary
