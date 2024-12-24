from app.persistence.repository import MemoryRepository
from app.models.post import Post
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.schema.posts import GetModel

class HBNBFacade:
    def __init__(self):
        self.post_repo = MemoryRepository(Post)

    async def get_posts(self, db: AsyncSession):
        return await self.post_repo.get_all(session=db)

    async def get_post(self, post_id, db: AsyncSession):
        return await self.post_repo.get(obj_id=post_id, session=db)

    async def create_post(self, post: GetModel, db: AsyncSession):
        new_post_data = post.dict() 
        new_post = Post(**new_post_data)
        await self.post_repo.create(obj=new_post, session=db)
        return new_post

    async def update_post(self, post_id, post: GetModel, db: AsyncSession):
        new_post_data = post.dict()
        newPost = Post(**new_post_data)
        await self.post_repo.update(obj_id=post_id, obj=newPost, session=db)
        return newPost
    
    async def delete_post(self, post_id, db: AsyncSession):
        return await self.post_repo.delete(obj_id=post_id, session=db)