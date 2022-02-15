from pyexpat import model
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix='/comment', tags=['Comment'])


@router.get('/{post_id}')
def get_comment(post_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    comment = db.query(models.Comment).filter(
        models.Comment.post_id == post_id).all()

    return comment


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def create_post(comment: schemas.Comment, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(
        models.Post.id == comment.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id : {comment.post_id} does not exist')
    comment_query = db.query(models.Comment).filter(models.Comment.post_id ==
                                                    comment.post_id, models.Comment.user_id == current_user.id)

    found_comment = comment_query.first()

    if found_comment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already commented on post {comment.post_id}')
    new_comment = models.Comment(user_id=current_user.id, **comment.dict())

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.put('/{id}')
def update_comment(id: int, updated_comment: schemas.CommentUpdate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comment).filter(
        models.Comment.id == id)

    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not Authorized to perform requested action')

    comment_query.update(updated_comment.dict(), synchronize_session=False)

    db.commit()

    return comment_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not Authorized to perform requested action')

    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
