#type: ignore
from fastapi import status, HTTPException, Depends, Form, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app import models, schemas, utils

router = APIRouter(
    tags=["User"]
)

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: Annotated[schemas.CreateUser, Form()], db:Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user