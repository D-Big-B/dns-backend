from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    super_server_id = Column(Integer, ForeignKey(
        'super_servers.id', ondelete='CASCADE'), nullable=False)

    owner = relationship('User')
    super_server = relationship('SuperServer')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    comment = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class SuperServer(Base):
    __tablename__ = "super_servers"

    id = Column(Integer, primary_key=True, nullable=False)
    server_name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete='CASCADE'), primary_key=True)


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, nullable=False)
    question = Column(String, nullable=False, unique=True)

    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    super_server_id = Column(Integer, ForeignKey(
        'super_servers.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    owner = relationship('User')
    super_server = relationship('SuperServer')


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, nullable=False)
    answer = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    query_id = Column(Integer, ForeignKey(
        'queries.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    owner = relationship('User')
    query = relationship('Query')
