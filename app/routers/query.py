
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/query',
    tags=['Query']

)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_query(query: schemas.Query, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    new_query = models.Query(owner_id=current_user.id, **query.dict())
    db.add(new_query)
    db.commit()
    db.refresh(new_query)

    return new_query


@router.get('/{server_id}', response_model=List[schemas.QueryOut])
def get_user(server_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    queries = db.query(models.Query).filter(
        models.Query.super_server_id == server_id).all()

    if not queries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'queries in server_id : {id} does not exist')

    return queries


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_query(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    query_query = db.query(models.Query).filter(models.Query.id == id)
    query = query_query.first()

    if query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"query with id: {id} does not exist")

    if query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not Authorized to perform requested action')

    query_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.QueryOut)
def update_query(id: int, updated_query: schemas.QueryUpdate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    query_query = db.query(models.Query).filter(
        models.Query.id == id)

    query = query_query.first()

    if query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"query with id: {id} does not exist")

    if query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not Authorized to perform requested action')

    query_query.update(updated_query.dict(), synchronize_session=False)

    db.commit()

    return query_query.first()
