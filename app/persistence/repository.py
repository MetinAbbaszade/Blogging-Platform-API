from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID
import json

class IRepository(ABC):
    @abstractmethod
    def get(self, obj_id):
        ...

    @abstractmethod
    def get_all(self):
        ...

    @abstractmethod
    def create(self, obj):
        ...

    @abstractmethod
    def update(self, obj_id, obj):
        ...

    @abstractmethod
    def delete(self, obj_id):
        ...

class MemoryRepository(IRepository):

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: str, session: AsyncSession):
        try:
            if isinstance(obj_id, UUID):
                pass
            else:
                obj_id = UUID(obj_id)
        except ValueError:
            raise ValueError("Invalid UUID format for user ID")
        
        return session.execute(select(self.model).where(obj_id == self.model.id)).scalars().first()

    async def get_all(self, session: AsyncSession):
        result = session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj, session: AsyncSession):
        if isinstance(obj.tags, list):
            obj.tags = json.dumps(obj.tags)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    async def update(self, obj_id, obj, session: AsyncSession):
        existing_obj = await self.get(obj_id=obj_id, session=session)
        obj_data = obj.dict(exclude_unset=True)

        for key, value in obj_data.items():
            setattr(existing_obj, key, value)

        session.commit()
        session.refresh(existing_obj)
        return existing_obj

    async def delete(self, obj_id, session: AsyncSession):
        object = await self.get(obj_id = obj_id, session = session)
        session.delete(object)
        session.commit()
        return object