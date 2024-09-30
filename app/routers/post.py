# type:ignore
from fastapi import Response, status, HTTPException, Depends, Form, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Annotated
from app.database import get_db
from app import models, schemas, oauth2
from typing import Any, Optional

router = APIRouter(
    tags=["Post"]
)


my_posts = [
    {
        "id": 1,
        "title": "FastApi",
        "content": "Fast Api Development"
    },
    {
        "id": 2,
        "title": "Streamlit",
        "content": "Streamlit Development"
    }
]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        else:
            print("No Data Found with the id:", id)


def find_post_index(id: int):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
        return None


@router.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db), get_current_users: int = Depends(oauth2.get_current_user), limit: int = 2, skip: int = 0, search: Optional[str] = ''):
    # cursor.execute("""SELECT *  FROM "Post" """)
    # posts = cursor.fetchall()
    # print(limit)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print("Log ===========> Post: ", posts, "Log===================> Type of Post" , type(posts))

    # results = db.query(models.Post, func.count(models.Vote.posts_id).label('Votes')).join(
    #     models.Vote, models.Vote.posts_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    return posts

    # print("Log===============> Type of Postout",  type(results[0]), type(schemas.PostOut))


@router.post("/createposts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: Annotated[schemas.PostCreate, Form()], db: Session = Depends(get_db), get_current_users: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO "Post" (title, content, publish) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.Publish))
    # my_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title = post.title, content = post.content, publish = post.Publish)
    print("LOG===>", get_current_users)
    new_post = models.Post(owner_id=get_current_users.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post

    # print(post.title)
    # print(post.content)
    # print(post)
    # # print(post.dict())
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)
    return {"Data": "Post Created"}


@router.get("/latest")
def get_latest():
    post = my_posts[len(my_posts)-1]
    return post


@router.get("/posts/{id}", response_model=schemas.Post)
def get_posts(id: int, response: Response, db: Session = Depends(get_db), get_current_users: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM "Post" WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(
        models.Post.id == id).first()  # type: ignore
    print(post)
    # # print(type(id))
    # post_name = find_post(id)
    # print(type(id))
    # print("post ", post_name)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"message": f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), get_current_users: Any = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM "Post" WHERE id = %s returning *""", (str(id)))
    # # print("Hello ", name)
    # delete_posts = cursor.fetchone()
    # conn.commit()

    delete_posts = db.query(models.Post).filter(
        models.Post.id == id)  # type: ignore
    post = delete_posts.first()
    if post is None:  # Check if the post was found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    if post.owner_id != get_current_users.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    delete_posts.delete(synchronize_session=False)
    db.commit()

    # delete_posts = my_posts.pop(index)
    # print("Delete index: ", index)
    # print("Delete pop: ", delete_posts)
    return Response(f"Post deleted with id: {id}", status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def updated_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), get_current_users: Any = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE "Post" SET title = %s, content=%s, publish=%s WHERE id = %s returning *""", (post.title, post.content, post.publish, str(id)))
    # update_posts = cursor.fetchone()
    # conn.commit()
    # index = find_post_index(id)

    post_query = db.query(models.Post).filter(
        models.Post.id == id)  # type: ignore
    update_posts = post_query.first()
    if update_posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    if update_posts.owner_id != get_current_users.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()
