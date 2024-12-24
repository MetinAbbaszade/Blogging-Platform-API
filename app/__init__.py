from sqlmodel import SQLModel
from fastapi import FastAPI
from sqlalchemy import create_engine
from app.api.v1.endpoints.posts import router as post_ns

URL = 'mysql+pymysql://root:M3tin190534@localhost/Post_Database'

engine = create_engine(url=URL, echo=True)

def create_app():
    app = FastAPI()

    app.include_router(post_ns)
    return app


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)