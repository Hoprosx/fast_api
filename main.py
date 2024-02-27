from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "i like pizza", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"posts": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-2:]
    return {"post": post}


@app.get("/posts/{id}")
async def get_post(id: int):
    return {"post": find_post(id)}


@app.post("/posts")
async def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"post": post_dict}
