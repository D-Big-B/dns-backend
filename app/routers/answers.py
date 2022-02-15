
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/answers',
    tags=['Answers']

)


@router.post('/{query_id}', status_code=status.HTTP_201_CREATED)
def create_answer(query_id: int, answer: schemas.Answer, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    new_answer = models.Answer(owner_id=current_user.id,
                               query_id=query_id, **answer.dict())
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer


@router.get('/{query_id}', response_model=List[schemas.AnswerOut])
def get_user(query_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    answers = db.query(models.Answer).filter(
        models.Answer.query_id == query_id).all()

    if not answers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'answers in query_id : {id} does not exist')

    return answers


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    answer_query = db.query(models.Answer).filter(models.Answer.id == id)
    answer = answer_query.first()

    if answer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"answer with id: {id} does not exist")

    if answer.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not Authorized to perform requested action')

    answer_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_query(id: int, updated_answer: schemas.QueryUpdate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    answer_query = db.query(models.Query).filter(
        models.Query.id == id)

    answer = answer_query.first()

    if answer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"answer with id: {id} does not exist")

    if answer.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not Authorized to perform requested action')

    answer_query.update(updated_answer.dict(), synchronize_session=False)

    db.commit()

    return answer_query.first()
