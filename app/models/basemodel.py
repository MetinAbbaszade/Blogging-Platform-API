from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime, timezone


class BaseClass(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_by: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_by = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_by": self.created_by.isoformat(),
            "updated_by": self.updated_by.isoformat(),
        }
