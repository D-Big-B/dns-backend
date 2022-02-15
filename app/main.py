from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import posts, users, auth, vote, comments, superServer, query, answers
from .config import settings

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(vote.router)
app.include_router(superServer.router)
app.include_router(comments.router)
app.include_router(query.router)
app.include_router(answers.router)


@app.get('/')
def root():
    return {'message': 'Hello World!'}
