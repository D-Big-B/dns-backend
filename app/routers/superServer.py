
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/superServer',
    tags=['Super Server']
)


@router.get('/', response_model=List[schemas.SuperServerOut])
def get_superServer(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    superServers = db.query(models.SuperServer).limit(limit).offset(skip).all()

    return superServers


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.SuperServerOut)
def create_superServer(superServer: schemas.SuperServer, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    new_superServer = models.SuperServer(**superServer.dict())

    db.add(new_superServer)
    db.commit()
    db.refresh(new_superServer)

    return new_superServer
