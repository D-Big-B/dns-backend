from datetime import datetime
from typing import Optional
from pydantic import BaseModel,  conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    super_server_id: int


class SuperServer(BaseModel):
    server_name: str


class SuperServerOut(BaseModel):
    id: int
    server_name: str
    created_at: datetime

    class Config:
        orm_mode = True


class Comment(BaseModel):
    comment: str
    post_id: int


class CommentUpdate(Comment):
    pass


class CommentOut(Comment):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    user_name: str
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    super_server_id: int
    owner: UserOut
    super_server: SuperServerOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    user_name: str
    password: str


class UserLogin(BaseModel):
    user_name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class VoteOut(BaseModel):
    post_id: int

    class Config:
        orm_mode = True


class Query(BaseModel):
    question: str
    super_server_id: int


class QueryUpdate(Query):
    pass


class QueryOut(BaseModel):
    id: int
    question: str
    created_at: datetime
    owner_id: int
    super_server_id: int
    owner: UserOut
    super_server: SuperServerOut

    class Config:
        orm_mode = True


class Answer(BaseModel):
    answer: str


class AnswerOut(Answer):
    id: int
    created_at: datetime
    owner_id: int
    query_id: int
    owner: UserOut
    query: QueryOut

    class Config:
        orm_mode = True
