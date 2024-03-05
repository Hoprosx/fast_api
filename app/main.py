import time

import psycopg
from fastapi import FastAPI, Response, status, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg.connect("dbname=fastapi user=postgres password=******", row_factory=dict_row)
        cursor = conn.cursor()
        print('Database connection was succesfull!')
        break
    except Exception as err:
        print(err)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    posts = cursor.execute("""SELECT * FROM posts""").fetchall()
    conn.commit()
    return {"posts": posts}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id desc""")
    posts = cursor.fetchmany(300)
    return {"latest posts": posts}


@app.get("/posts/{id}")
async def get_post(id: int):
    print(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute(f"""INSERT INTO posts (title, content, published)
                        VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    return {"post": new_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return {'data': updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
