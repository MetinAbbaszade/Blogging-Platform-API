from app.extensions import get_db
from fastapi import Depends, APIRouter, HTTPException, status
from app.api.v1.schema.posts import PostModel, GetModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from typing import List
from uuid import uuid4
from app.service import facade
from datetime import datetime
import json

router = APIRouter(prefix='/api/v1/post', tags=['Post'])


@router.get('/', response_model=List[GetModel], status_code=status.HTTP_200_OK)
async def get_all_posts(db: AsyncSession = Depends(get_db)):
    posts: List[Post] = await facade.get_posts(db=db)

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Posts are not found'
        )
    
    data = [post.to_dict() for post in posts] 

    return data
    

@router.get('/{post_id}', response_model=GetModel, status_code=status.HTTP_200_OK)
async def get_post(post_id: str, db: AsyncSession = Depends(get_db)):
    post: Post = await facade.get_post(post_id=post_id, db=db)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Post is not found'
        )
    
    return post.to_dict()


@router.post('/', response_model=PostModel, status_code=status.HTTP_201_CREATED)
async def create_post(model: GetModel, db: AsyncSession = Depends(get_db)):
    model.id = uuid4()
    model.created_by = datetime.now()
    model.updated_by = datetime.now()

    existing_post = await facade.get_post(post_id=model.id, db=db)
    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Post already exists'
        )
    
    added_post: Post = await facade.create_post(post=model, db=db)

    if isinstance(added_post.tags, str):
        added_post.tags = json.loads(added_post.tags)

    return {
        "title": added_post.title,
        "content": added_post.content,
        "category": added_post.category,
        "tags": added_post.tags
    }
    

@router.put('/{post_id}', response_model=PostModel, status_code=status.HTTP_200_OK)
async def update_post(post_id: str, model: GetModel, db: AsyncSession = Depends(get_db)):

    existing_post: Post = await facade.get_post(post_id=post_id, db=db)
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post does not exist'
        )
    
    model.id = post_id
    model.created_by = existing_post.created_by
    model.updated_by = datetime.now()

    updated_post: Post = await facade.update_post(post_id=post_id, post=model, db=db)

    if isinstance(updated_post.tags, str):
        updated_post.tags = json.loads(updated_post.tags)

    return {
        "title": updated_post.title,
        "content": updated_post.content,
        "category": updated_post.category,
        "tags": updated_post.tags
    }

@router.delete('/{post_id}', response_model=GetModel, status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, db: AsyncSession = Depends(get_db)):
    
    post: Post = await facade.get_post(post_id=post_id, db=db)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    
    deleted_post: Post = await facade.delete_post(post_id=post_id, db=db)

    return deleted_post.to_dict()