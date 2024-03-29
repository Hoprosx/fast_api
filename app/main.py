from fastapi import FastAPI

from app.database import engine
from . import models
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
