from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app import schemas, database, oauth2, models

router = APIRouter(
    tags = ['Vote']
)

@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} does not exist")
   
    vote_query = db.query(models.Vote).filter(models.Vote.posts_id == vote.post_id, models.Vote.users_id == current_user.id)
    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(posts_id = vote.post_id, users_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "Successfully added the vote"}
    else:
        if not found_vote:
            raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "successfully removed vote"}
